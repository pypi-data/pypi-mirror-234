import base64
import json
import logging
import threading
import time
from json import JSONDecodeError
from time import sleep

import requests

logger = logging.getLogger('echolog')


def unpack(request, default=None):
    request.raise_for_status()
    try:
        return json.loads(request.content)
    except (JSONDecodeError, UnicodeDecodeError):
        return request.content or default


def call_repeatedly_fail_safe(interval, func, *args, timeout=5):
    stopped = threading.Event()

    def loop():
        while not stopped.wait(interval):  # the first call is in `interval` secs
            while True:
                try:
                    func(*args)
                    break
                except Exception as exc:
                    logger.error(f'Failed to call {func.__name__} due to {exc}, retrying in {timeout}s')
                    sleep(timeout)

    t = threading.Thread(target=loop)
    t.daemon = True
    t.start()
    return stopped.set


class Us2Cognito:
    def __init__(self, api_url, username, password):
        self.api_url = api_url
        self.username = username
        self.password = password
        self.id_token = ''
        self.refresh_token = ''
        self.user = {}
        self.payload = {}
        self.exp = 0
        self.authenticate()
        time_till_exp = self.exp - time.time()
        self.stop_refresh = call_repeatedly_fail_safe(time_till_exp * 3 / 4, self.refresh)

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['stop_refresh']
        return self_dict

    def expired(self):
        return time.time() > self.exp

    def unpack_auth(self, request):
        data = unpack(request)
        auth = data['AuthenticationResult']
        self.id_token = auth['IdToken']
        self.refresh_token = auth.get('RefreshToken', self.refresh_token)
        self.payload = json.loads(base64.b64decode(self.id_token.split('.')[1] + '===').decode())
        self.exp = self.payload['exp']
        self.user = self.get_user()

    def get_user(self):
        return unpack(requests.get(f"{self.api_url}/users/current", headers=self.get_headers()))

    def authenticate(self):
        self.unpack_auth(
            requests.post(f"{self.api_url}/users/login", json={'username': self.username, 'password': self.password}),
        )

    def refresh(self):
        try:
            self.unpack_auth(
                requests.post(f"{self.api_url}/users/refresh", json={'refreshToken': self.refresh_token}),
            )
        except Exception as exc:
            logger.warning(f'Failed to renew token due to {exc}, re-authenticating')
            self.authenticate()

    def customer(self):
        groups = self.user.get('permissions', [])
        s3 = [g for g in groups if g.startswith('s3-')]
        if s3:
            return s3[0].split('-', 1)[1]
        if 'upload' in groups or 'admin' in groups:
            return self.user.get('cognito_id')

    def regions(self):
        groups = self.user.get('permissions', [])
        return [r.split('-', 1)[1] for r in groups if r.startswith('region-') and 'global' not in r]

    def get_headers(self):
        return {"Authorization": f"Bearer {self.id_token}"}

    def get_cookies(self):
        return {".idToken": self.id_token}

    def close(self):
        self.stop_refresh()
