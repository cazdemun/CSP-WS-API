############
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#############

from datetime import datetime
import os.path
import websockets 
import ssl
import json
import logging

# Set up logging for websockets library
wslogger = logging.getLogger('websockets')
wslogger.setLevel(logging.INFO)
wslogger.addHandler(logging.StreamHandler())

logger = logging.getLogger('cortex')
# logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class CortexApiException(Exception):
    pass

class Cortex(object):
    CORTEX_URL = "wss://localhost:6868"

    def __init__(self, client_id_file_path):
        self.parse_credentials(client_id_file_path)
        self.websocket = None
        self.auth_token = None
        self.packet_count = 0
        self.id_sequence = 0

    def parse_credentials(self, client_id_file_path):
        self.client_id = None
        self.client_secret = None
        self.license_id = None
        if not os.path.exists(client_id_file_path):
            raise OSError("no such file: {}".format(client_id_file_path))
        with open(client_id_file_path, 'r') as client_id_file:
            for line in client_id_file:
                if line.startswith('#'):
                    continue
                (key, val) = line.split(' ')
                if key == 'client_id':
                    self.client_id = val.strip()
                elif key == 'client_secret':
                    self.client_secret = val.strip()
                elif key == 'license_id':
                    self.license_id = val.strip()
                else:
                    raise ValueError(
                        f'Found invalid key "{key}" while parsing '
                        f'client_id file {client_id_file_path}')

        if not self.client_id or not self.client_secret or not self.license_id:
            raise ValueError(
                f"Did not find expected keys in client_id file "
                f"{client_id_file_path}")

    def gen_request(self, method, auth, **kwargs):
        self.id_sequence += 1
        params = {key: value for (key, value) in kwargs.items()}
        if auth and self.auth_token:
            params['cortexToken'] = self.auth_token
        request = json.dumps(
            {'jsonrpc': "2.0",
            'method': method,
            'params': params,
            'id': self.id_sequence
            })
        logger.debug(f"Sending request:\n{request}")
        return request

    async def init_connection(self):
        ''' Open a websocket and connect to cortex.  '''
        # Cortex is running locally; data is encrypted, but the certificate is
        # self-signed.
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        self.websocket = await websockets.connect(
            self.CORTEX_URL, ssl=ssl_context)

    async def send_command(self, method, auth=True, callback=None, **kwargs):
        if not self.websocket:
            await self.init_connection()
        if auth and not self.auth_token:
            await self.authorize()
        msg = self.gen_request(method, auth, **kwargs)
        await self.websocket.send(msg)
        logger.debug("sent; awaiting response")
        resp = await self.websocket.recv()
        if 'error' in resp:
            logger.warn(f"Got error in {method} with params {kwargs}:\n{resp}")
            raise CortexApiException(resp)
        resp = json.loads(resp)
        if callback:
            callback(resp)
        return resp

    async def get_data(self):
        resp = await self.websocket.recv()
        logger.debug(f"get_data got {resp}")
        self.packet_count += 1
        return resp

    async def close(self):
        ''' Close the cortex connection '''
        await self.websocket.close()

    ##
    # Here down are cortex specific commands
    # Each of them is documented thoroughly in the API documentation:
    # https://emotiv.gitbook.io/cortex-api
    ##
    async def authorize(self, license_id=None, debit=None):
        params = {'clientId': self.client_id,
                  'clientSecret': self.client_secret}
        if license_id:
            params['license'] = self.license_id
        if debit:
            params['debit'] = debit

        resp = await self.send_command('authorize', auth=False, **params)
        logger.debug(f"{__name__} resp:\n{resp}")
        self.auth_token = resp['result']['cortexToken']

    async def query_headsets(self):
        resp = await self.send_command('queryHeadsets', auth=False)
        self.headsets = [h['id'] for h in resp['result']]
        logger.debug(f"{__name__} found headsets {self.headsets}")
        logger.debug(f"{__name__} resp:\n{resp}")

    async def create_session(self, activate, headset_id=None):
        status = 'active' if activate else 'open'
        if not headset_id:
            headset_id = self.headsets[0]
        params = {'cortexToken': self.auth_token,
                  'headset': headset_id,
                  'status': status}
        resp = await self.send_command('createSession', **params)
        self.session_id = resp['result']['id']
        logger.debug(f"{__name__} resp:\n{resp}")
        print(f"Session created - cortex.py")

    async def close_session(self):
        params = {'cortexToken': self.auth_token,
                  'session': self.session_id,
                  'status': 'close'}
        resp = await self.send_command('updateSession', **params)
        logger.debug(f"{__name__} resp:\n{resp}")

    async def subscribe(self, stream_list):
        params = {'cortexToken': self.auth_token,
                  'session': self.session_id,
                  'streams': stream_list}
        resp = await self.send_command('subscribe', **params)
        logger.debug(f"{__name__} resp:\n{resp}")

    async def unsubscribe(self, stream_list):
        params = {'cortexToken': self.auth_token,
                  'session': self.session_id,
                  'streams': stream_list}
        resp = await self.send_command('unsubscribe', **params)
        logger.debug(f"{__name__} resp:\n{resp}")