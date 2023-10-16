import base64
from . import *
import os
import logging

log = logging.getLogger(LOGGER_NAME)


class Authenticator:
    def __init__(self):       
        self.token = os.getenv('NG_API_AUTHTOKEN')
        self.api_key = os.getenv('NG_API_KEY')
        self.login = os.getenv('LOGIN')
        self.password = os.getenv('PASSWORD')

    def get_token(self):
        if self.token is not None:
            log.debug('Authentication with Web Token ...')
            return {'Authorization': f'Bearer {self.token}'}
        
        elif self.api_key is not None:
            log.debug('Authentication with API Key ...')
            return {'Authorization': f'ApiKey {self.api_key}'}

        else:
            if self.login is not None and self.password is not None:
                log.debug('Authentication with Credentials ...')
                credentials = self.login + ":" + self.password
                message_bytes = credentials.encode('ascii')
                base64_enc = base64.b64encode(message_bytes).decode('UTF-8')

                d = {'Authorization': f"Basic {base64_enc}"}
                return d

            else:
                log.error('No login or password provided, neither token can be read from environment variable.')
                raise Exception('Authentication issue : no credentials found')
