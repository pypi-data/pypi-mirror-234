import logging
import os
import random
import socket
import string

import pysftp
from dateutil import parser
from hl7apy.core import Message, Segment, Field
from hl7apy.parser import parse_message

logger = logging.getLogger('echolog')


def convert_dt(dt_string, dt_format):
    if not dt_string:
        return ""

    try:
        dt = parser.parse(dt_string)
        return dt.strftime(dt_format)

    except Exception as ex:
        logger.error(f'Failed to convert dt, {dt_string}, {dt_format}, {ex}')
        return ""


class Hl7:
    def __init__(self, vendor_config, message_type, version):
        self.vendor_config = vendor_config
        self.msg_control_id = ""

        self.message = Message(message_type, version=version)

    def generate(self, study_data, measurements, report_type, report_pdf_encoded):
        vendor_config = self.vendor_config

        logger.debug("HL7 generation started")

        is_invalid_report_pdf = not report_pdf_encoded
        is_invalid_measurements = not measurements or len(measurements) == 0

        if report_type == "PDF" and is_invalid_report_pdf:
            logger.warning("Failed to generate HL7 - Report PDF is invalid")
            return False

        if report_type == "TEXT" and is_invalid_measurements:
            logger.warning("Failed to generate HL7 - Invalid measurements")
            return False

        if report_type == "ALL" and is_invalid_report_pdf and is_invalid_measurements:
            logger.warning("Failed to generate HL7 - Invalid measurements or invalid Report PDF")
            return False

        study_tags = study_data.get("tags") or {}
        study_date = study_tags.get("StudyDate") or ""
        study_time = study_tags.get("StudyTime") or ""
        study_dt = f"{study_date}{study_time.split('.')[0] if study_time else ''}"
        accession_no = study_tags.get("AccessionNumber") or ""
        patient_id = study_tags.get("PatientID") or ""

        random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        self.msg_control_id = f'{accession_no or patient_id or ""}__{random_id}'

        message = self.message  # Message("ORU_R01", version="2.5")
        message.msh.msh_3 = vendor_config.get("sending_app", "Us2.ai")  # sending application
        message.msh.msh_4 = vendor_config.get("sending_facility", "Us2 Cloud")  # sending facility
        message.msh.msh_5 = vendor_config.get("receiving_app", "")  # Receiving app - Should read from UI
        message.msh.msh_6 = vendor_config.get("receiving_facility", "")  # Receiving Facility
        message.msh.msh_9 = "ORU^R01^ORU_R01"  # message type
        message.msh.msh_10 = self.msg_control_id  # msg control ID
        message.msh.msh_11 = vendor_config.get("processing_type", "T")
        message.msh.msh_16 = vendor_config.get("ack_type", "AL")

        patient_id = study_data.get("patientID") or ""
        gender = study_data.get("gender") or ""
        dob = study_data.get("dob") or ""
        processed_date = study_data.get("processedDate") or ""
        report_status = 'F' if study_data.get("approved", False) else 'P'

        dob_formatted = convert_dt(dob, "%Y%m%d")
        pd_formatted = convert_dt(processed_date, "%Y%m%d%H%M")

        pid = Segment("PID")
        pid.pid_2.pid_2_1 = patient_id  # Patient ID   study_data.get("", "")
        pid.pid_3.pid_3_1 = patient_id  # Patient ID
        pid5 = Field("PID_5")
        pid5.pid_5_1 = study_data.get("lastName") or ""  # Family name
        pid5.pid_5_2 = study_data.get("firstName", "") or ""  # Given name
        pid.add(pid5)
        pid.pid_6 = ""  # Mothers maiden name
        pid.pid_7 = dob_formatted
        pid.pid_8 = study_data.get("gender", "") or ""
        pid11 = Field("PID_11")
        pid11.pid_11_1 = ""  # Street address
        pid11.pid_11_3 = ""  # City
        pid11.pid_11_4 = ""  # State
        pid11.pid_11_5 = ""  # zip
        pid.add(pid11)
        pid.pid_13 = ""  # Phone #
        pid.pid_18 = patient_id  # Patient Account #
        pid.pid_19 = ""  # Patient SSN
        message.add(pid)

        message.orc.orc_1 = "RE"
        message.orc.orc_2 = accession_no  # Accession_no
        message.orc.orc_3 = accession_no  # Accession_no
        message.orc.orc_5 = ""  # Study desc
        message.orc.orc_7 = study_dt  # Observation Date & Time

        message.obr.obr_1 = "1"
        message.obr.obr_2 = accession_no  # Accession_no
        message.obr.obr_3 = accession_no  # Accession_no
        message.obr.obr_4.obr_4_1 = ""  # Universal Service Identifier - appointment type code
        message.obr.obr_4.obr_4_2 = ""  # Study desc
        message.obr.obr_7 = study_dt  # Observation Date & Time
        message.obr.obr_20 = ""  # Modality
        message.obr.obr_22 = pd_formatted  # Approved Date & Time
        message.obr.obr_24 = ""  # Modality
        # https://hl7-definition.caristix.com/v2/HL7v2.5/Tables/0123
        message.obr.obr_25 = "R"  # Result status - F - Final, R - store, but not verified, etc..,
        message.obr.obr_31 = ""  # Study desc

        obx_index = 1
        is_pdf_requested = report_type == "ALL" or report_type == "PDF"

        if not is_invalid_report_pdf and is_pdf_requested:
            logger.debug("Embedding Report PDF into OBX")

            obx = Segment("OBX")
            obx.obx_1 = str(obx_index)  # Observation Set ID
            obx.obx_2 = "ED"  # Observation Set ID
            obx.obx_3.obx_3_1 = ""  # Observation Identifier
            obx.obx_3.obx_3_2 = ""  # Study desc

            if vendor_config.get("report_pdf_format", "SIMPLE") == "SIMPLE":
                obx.obx_5 = report_pdf_encoded  # Observation result
            else:
                obx.obx_5 = f"pdf^TEXT^^Base64^{report_pdf_encoded}"

            # Observation result status https://hl7-definition.caristix.com/v2/HL7v2.5/Tables/0085
            obx.obx_11 = report_status
            obx.obx_14 = study_dt  # Observation Date & Time
            obx.obx_19 = pd_formatted

            message.add(obx)
            obx_index += 1

        if report_type == "ALL" or report_type == "TEXT":
            logger.debug("Adding measurements into OBX")

            for code in measurements.keys():
                proto = measurements[code]["proto"]
                m_value = measurements[code]["m_value"]

                ref_range = ""
                value = m_value.get('value')

                try:
                    value = str(round(value, proto.get('decimalPlaces')))
                    ref_object = [str(guideline['lo']) + '-' + str(guideline['hi'])
                                  for guideline in proto.get('guidelines')
                                  if guideline.get('gender') == (gender if gender != "" and gender is not None else "F")
                                  ]

                    ref_range = ref_object[0] if len(ref_object) == 1 else ""

                except Exception as ex:
                    logger.warning(f'Failed to calculate measurement values/ref range. Value: {value}, {ex}')
                    value = str(value)

                obx = Segment("OBX")
                obx.obx_1 = str(obx_index)  # Observation Set ID
                obx.obx_2 = "NM"  # Observation Set ID
                obx.obx_3.obx_3_1 = str(code)
                obx.obx_3.obx_3_2 = proto.get('name')
                obx.obx_5 = value
                obx.obx_6 = proto.get('unit')
                obx.obx_7 = ref_range
                obx.obx_8 = ""  # Abnormal flags
                obx.obx_11 = report_status
                obx.obx_14 = study_dt  # Observation Date & Time
                obx.obx_19 = pd_formatted  # Analysis time - processed dt

                message.add(obx)
                obx_index += 1

        logger.debug("HL7 generation completed")
        return self.msg_control_id

    def send(self):
        vendor_config = self.vendor_config
        logger.debug(f'Sending HL7 to vendor. Mode: {vendor_config.get("transfer_mode")}')

        if vendor_config.get("transfer_mode") == "MLLP":
            msg_to_send = self.message.to_mllp()

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                sock.connect((vendor_config.get('host'), int(vendor_config.get('port', "22"))))
                sock.sendall(msg_to_send.encode('UTF-8'))

                logger.info(f'HL7(MLLP) sent successfully. ID: {self.msg_control_id}')

                received = sock.recv(1024 * 1024)
                ack_msg = received.decode().strip()
                msg = parse_message(ack_msg, find_groups=True, validation_level=2)

                if msg.children[1] and msg.children[1].children[0]:
                    logger.info(f'Received ack code: {msg.children[1].children[0].value}')

                logger.debug(f'Received ack. ID: {self.msg_control_id}, msg: {ack_msg}')

                return received

            except Exception as ex:
                logger.error(f'Failed to send HL7(MLLP): {self.msg_control_id}, {vendor_config.get("host")}, ex: {ex}')

            finally:
                sock.close()

        elif vendor_config.get("transfer_mode") == "SFTP":
            hl7_string = self.message.to_er7()

            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None

            try:
                with pysftp.Connection(vendor_config.get("host"),
                                       port=int(vendor_config.get("port")),
                                       username=vendor_config.get("username"),
                                       password=vendor_config.get("password"),
                                       private_key=vendor_config.get("private_key_file"),
                                       cnopts=cnopts,
                                       ) as sftp:

                    sftp.cwd(vendor_config.get("root_path"))
                    file = sftp.open(f'{self.msg_control_id}.hl7', 'wb')
                    file.write(hl7_string)

                    logger.info(f'HL7(SFTP) sent successfully. ID: {self.msg_control_id}')

            except Exception as ex:
                logger.error(f'Failed to send HL7(SFTP): {self.msg_control_id}, {vendor_config.get("host")}, ex: {ex}')

        elif vendor_config.get("transfer_mode") == "FILE":
            hl7_string = self.message.to_er7()

            try:
                full_path = os.path.join(vendor_config.get("root_path"), f"{self.msg_control_id}.hl7")
                file = open(full_path, "a")
                file.write(hl7_string)
                file.close()

                logger.info(f'HL7(File) was written successfully.. ID: {self.msg_control_id}, File: {full_path}')

            except Exception as ex:
                logger.error(f'Failed to write HL7. ID: {self.msg_control_id}, {vendor_config.get("host")}, ex: {ex}')
