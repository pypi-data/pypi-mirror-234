import base64
import datetime
import io
import itertools
import logging
import ssl
import threading
import time
from collections import defaultdict
from functools import cached_property

import requests
from dateutil import parser
from pathy import Pathy
from pydicom import dcmread
from pynetdicom import AE

from echoloader.hl7 import Hl7
from echoloader.login import unpack

logger = logging.getLogger('echolog')
DEFAULT_AE_TITLE = "Us2.ai"


def server_context(ca, cert, key):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=cert, keyfile=key)
    context.load_verify_locations(cafile=ca)
    # Only TLS <= 1.2 is supported, make sure we always use this
    context.minimum_version = context.maximum_version = ssl.TLSVersion.TLSv1_2

    return context


def client_context(ca, cert, key):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=ca)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_cert_chain(certfile=cert, keyfile=key)
    context.check_hostname = False

    return context


class PacsConnection:
    def __init__(self, details):
        self.store_on_filesystem = True
        self.host = self.port = self.remote_ae_title = self.local_ae_title = self.cert = self.key = None
        self.details = details
        parts = details.split(':')
        if len(parts) > 2:
            self.store_on_filesystem = False
            self.host, port, self.remote_ae_title = parts[:3]
            self.local_ae_title = parts[3] if len(parts) > 3 else DEFAULT_AE_TITLE
            self.ca, self.cert, self.key = parts[4:7] if len(parts) > 5 else (None, None, None)
            self.port = int(port)

    def store(self, ds, called_ae):
        if self.store_on_filesystem:
            dst = Pathy.fluid(self.details) / ds.PatientID / f"{ds.SOPInstanceUID}.dcm"
            dst.parent.mkdir(exist_ok=True, parents=True)
            ds.save_as(str(dst), write_like_original=False)
            return
        ae = AE(ae_title=self.local_ae_title)
        ae.add_requested_context(ds.SOPClassUID, ds.file_meta.TransferSyntaxUID)

        remote_ae = called_ae or self.remote_ae_title
        assoc = ae.associate(self.host, self.port, ae_title=remote_ae,
                             tls_args=(client_context(self.ca, self.cert, self.key), None) if self.cert else None)

        if not assoc.is_established:
            raise ConnectionError('Association rejected, aborted or never connected')
        # Use the C-STORE service to send the dataset
        # returns the response status as a pydicom Dataset
        try:
            # force treat context as supporting the SCP role
            for cx in assoc.accepted_contexts:
                cx._as_scp = True

            status = assoc.send_c_store(ds)

            # Check the status of the storage request
            if status:
                # If the storage request succeeded this will be 0x0000
                logger.debug(f'C-STORE request status: 0x{status.Status:04x}')
            else:
                raise ValueError('Connection timed out, was aborted or received invalid response')
        finally:
            # Release the association
            assoc.release()

    def __str__(self):
        return self.details


class Sync(threading.Thread):
    def __init__(self, cmd, pool, *vargs, **kwargs):
        super().__init__(*vargs, **kwargs)
        self.args = cmd
        self.by_measurement = cmd.sync_by_measurement
        self.connections = cmd.sync
        self.auth = cmd.auth
        self.api_url = self.auth.api_url
        self.uploader = self.auth.username
        self.killed = False
        self.params = {'v': cmd.v}
        self.sync_from = eval(cmd.sync_from).replace(tzinfo=datetime.timezone.utc)
        self.last_sync = {}
        self.modalities = cmd.sync_modalities
        self.poll = cmd.sync_poll
        self.sr_params = {}
        self.doc_params = {}
        self.pdf_params = {}
        self.pool = pool
        self.search_params = {k: v for e in cmd.sync_search for k, v in [e.split('=', 1)]}
        self.protocol = unpack(requests.get(
            f'{self.api_url}/sync/protocol', params=self.params, headers=self.auth.get_headers()))['current_protocol']
        if cmd.sync_url:
            self.sr_params['url'] = True
        if cmd.sync_main_findings:
            self.sr_params['main_findings'] = True
            self.doc_params['main_findings'] = True
            self.pdf_params['main_findings'] = True
        if cmd.sync_pdf_images:
            self.doc_params['image'] = True
            self.pdf_params['image'] = True
        if cmd.sync_designators:
            self.sr_params['designators'] = cmd.sync_designators
        if cmd.sync_mapping:
            self.sr_params['mapping'] = cmd.sync_mapping
        if cmd.sync_regulatory_status:
            self.sr_params['regulatory_status'] = True
        if cmd.sync_edited_status:
            self.sr_params['edited_status'] = True
        if cmd.sync_annotations:
            self.sr_params['annotations'] = True
        self.doc_params['dicom_encapsulated_pdf'] = True
        self.ps_params = {}
        self.sc_params = {}

    def latest_mod(self, sid):
        resp = unpack(requests.get(
            f"{self.api_url}/sync/modification/{sid}",
            params={**self.params, 'limit': 1},
            headers=self.auth.get_headers()))
        mods = resp['results'] if isinstance(resp, dict) else resp
        return mods[-1]

    def stop(self):
        self.killed = True

    def handle_study_sync_error(self, err, sid):
        logger.error(f'Failed to sync study {sid} due to {err}')

    def sync(self):
        filter_params = {
            **self.params,
            'uploader': self.uploader,
            'lastUpdatedFrom': max([self.sync_from, *self.last_sync.values()]),
            **self.search_params,
        }
        res = unpack(
            requests.get(f'{self.api_url}/study/search', params=filter_params, headers=self.auth.get_headers()), {})
        results = res.get('results', [])
        for study in results:  # All search results have been updated since we last checked -> sync everything
            sid = study['id']
            last_sync = self.last_sync.get(sid, self.sync_from)
            logger.info(f'Syncing {sid} for changes since {last_sync}')
            mod = self.latest_mod(sid)
            creation = parser.parse(mod['creation']).replace(tzinfo=datetime.timezone.utc)
            self.last_sync[sid] = creation
            sync = SyncWorker(self, study, last_sync)
            self.pool.apply_async(sync.sync_study, error_callback=lambda err: self.handle_study_sync_error(err, sid))

    def run(self) -> None:
        while not self.killed:
            try:
                self.sync()
            except Exception as exc:
                logger.error(f'Failed sync due to: {exc}')
            time.sleep(self.poll)


class SyncWorker:
    def __init__(self, worker: Sync, study, t):
        self.api_url = worker.api_url
        self.auth = worker.auth
        self.args = worker.args
        self.params = worker.params
        self.sr_params = worker.sr_params
        self.doc_params = worker.doc_params
        self.pdf_params = worker.pdf_params
        self.ps_params = worker.ps_params
        self.sc_params = worker.sc_params
        self.protocol = worker.protocol
        self.modalities = worker.modalities
        self.by_measurement = worker.by_measurement
        self.connections = worker.connections
        self.hl7_config = worker.auth.user.get('dicom_router_config', {}).get('hl7_config', {})
        self.study = study
        self.sid = study['id']
        self.t = t

    def sr(self):
        return requests.get(f"{self.api_url}/study/sr/{self.sid}", headers=self.auth.get_headers(),
                            params={**self.params, **self.sr_params})

    def ds(self):
        ds = defaultdict(dict)
        for mod in self.mods:
            if mod['model'] == 'dicom.dicom':
                pk = mod['obj_pk']
                ds[pk].update(mod['new_fields'])
                ds[pk]['last_update'] = parser.parse(mod['creation']).replace(tzinfo=datetime.timezone.utc)
                if mod['action'] == 'delete' and pk in ds:
                    del ds[pk]
        for k, d in ds.items():
            if d['last_update'] > self.t and not d.get('from_dicom_id') and d.get('output_path'):
                yield requests.get(f"{self.api_url}/dicom/ds/{k}", headers=self.auth.get_headers(),
                                   params={**self.params})

    def ps(self, ms):
        return requests.get(f"{self.api_url}/dicom/ps", headers=self.auth.get_headers(),
                            params={**self.params, **self.ps_params, 'measurements': ms})

    def sc(self, ms):
        return requests.get(f"{self.api_url}/dicom/sc", headers=self.auth.get_headers(),
                            params={**self.params, **self.sc_params, 'measurements': ms})

    def doc(self):
        return requests.get(f"{self.api_url}/study/pdf/{self.sid}", headers=self.auth.get_headers(),
                            params={**self.params, **self.doc_params})

    def pdf(self):
        return requests.get(f"{self.api_url}/study/pdf/{self.sid}", headers=self.auth.get_headers(),
                            params={**self.params, **self.pdf_params})

    @cached_property
    def mods(self):
        params = {**self.params, 'page': 1, 'page_size': 10_000}
        result = []
        count = 1
        while len(result) < count:
            mods = unpack(requests.get(
                f"{self.api_url}/sync/modification/{self.sid}", params=params, headers=self.auth.get_headers()))
            result.extend(mods['results'] if isinstance(mods, dict) else mods)
            count = mods['count'] if isinstance(mods, dict) else len(mods)
            params['page'] += 1
        return result

    def read_measurements(self):
        ms = defaultdict(dict)
        for mod in self.mods:
            if mod['model'] == 'measurement.measurements':
                pk = mod['obj_pk']
                ms[pk].update(mod['new_fields'])
                ms[pk]['last_update'] = parser.parse(mod['creation']).replace(tzinfo=datetime.timezone.utc)
                if mod['action'] == 'delete' and pk in ms:
                    del ms[pk]
        measurements = {}
        for m in ms.values():
            proto = self.protocol.get('measurements', {}).get(str(m.get('code_id')), {})
            if (proto.get('shouldDisplay')
                    and m.get('used')
                    and m.get('dicom_id')
                    and m.get('plot_obj')):
                measurements[m['code_id']] = {
                    "proto": proto,
                    "m_value": m,
                }
        return measurements

    def media(self):
        ms = defaultdict(dict)
        for mod in self.mods:
            if mod['model'] == 'measurement.measurements':
                pk = mod['obj_pk']
                ms[pk].update(mod['new_fields'])
                ms[pk]['last_update'] = parser.parse(mod['creation']).replace(tzinfo=datetime.timezone.utc)
                if mod['action'] == 'delete' and pk in ms:
                    del ms[pk]
        grouped = defaultdict(list)
        for m in ms.values():
            proto = self.protocol.get('measurements', {}).get(str(m.get('code_id')), {})
            if (proto.get('shouldDisplay')
                    and m['last_update'] > self.t
                    and m.get('used')
                    and m.get('dicom_id')
                    and m.get('plot_obj')):
                k = (m['dicom_id'], m['frame'], *([m['id']] if self.by_measurement else []))
                grouped[k].append(m['id'])
        for ms in grouped.values():
            if 'PS' in self.modalities:
                yield self.ps(ms)
            if 'SC' in self.modalities:
                yield self.sc(ms)

    def sync_hl7(self):
        measurements = {}
        report_pdf_encoded = None

        try:
            report_type = self.hl7_config.get('report_type', 'TEXT')
            if report_type != "PDF":
                measurements = self.read_measurements()
            if report_type != "TEXT":
                report_pdf_response = self.pdf()
                if report_pdf_response.status_code == 200:
                    report_pdf_encoded = base64.b64encode(report_pdf_response.content).decode("utf-8")
                else:
                    logger.error(f'Failed to fetch from {report_pdf_response.url} - {report_pdf_response.status_code}')

            hl7 = Hl7(self.hl7_config, "ORU_R01", "2.5")
            msg_control_id = hl7.generate(self.study, measurements, report_type, report_pdf_encoded)

            if msg_control_id:
                hl7.send()
            else:
                logger.warning(f'Failed to generate HL7 {msg_control_id}')
        except Exception as ex:
            logger.error(f'Failed to sync HL7 due to {ex}')

    def sync_study(self):
        for req in itertools.chain(
                self.media() if [m in self.modalities for m in ['PS', 'SC']] else [],
                self.ds() if 'DS' in self.modalities else [],
                [self.sr()] if 'SR' in self.modalities else [],
                [self.doc()] if 'DOC' in self.modalities else [],
        ):
            url = req.url
            try:
                bs = unpack(req)
            except Exception as exc:
                logger.error(f'Failed to fetch {url} due to {exc}')
                continue
            ds = dcmread(io.BytesIO(bs))
            for conn in self.connections:
                try:
                    called_ae = None
                    if self.args.customer_aet:
                        called_ae = self.study.get('customer')

                    conn.store(ds, called_ae)
                    logger.info(f'Synced {url} to {conn}')
                except Exception as exc:
                    logger.error(f'Failed to sync {url} due to {exc}')

        if self.hl7_config.get('enabled', False):
            self.sync_hl7()
