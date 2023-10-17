from keyring.backend import KeyringBackend, properties
from keyring.credentials import Credential
from keyring.errors import PasswordDeleteError, PasswordSetError
from typing import Any, Optional, Tuple
import os
import subprocess
import shutil
import json


class BitwardenCredential(Credential):
    def __init__(self, data: dict):
        super().__init__()
        self._data = data

    def __contains__(self, item):
        return item in self._retrieves_fields()

    def __getitem__(self, item):
        fields = self._retrieves_fields()
        return fields[item]

    def _retrieves_fields(self) -> dict:
        if 'fields' in self._data:
            return {f['name']: f['value'] for f in self._data['fields']}
        return {}

    @property
    def username(self):
        return self._data['login']['username']

    @property
    def password(self):
        return self._data['login']['password']

    def get(self, item) -> Optional[Any]:
        return self._retrieves_fields().get(item)


class BitwardenClient:
    @staticmethod
    def __read_master_password(pwd: str = None, **kwargs) -> Optional[str]:
        if pwd is not None:
            return pwd
        return None

    @staticmethod
    def __prepare_env(custom_env: dict = None):
        if custom_env is None:
            return os.environ
        env = os.environ.copy()
        for k, v in custom_env.items():
            env[k] = v
        return env

    def __init__(self, login: str, password: str = None, **kwargs):
        self._base_cmd = ['bw', '--nointeraction', '--response', '--pretty']
        self._login = login
        self._vault_url = kwargs.get('vault_url', 'null')

        master = self.__read_master_password(password, **kwargs)
        if master is None:
            ValueError("Missing master password to access to keyring")
        os.environ['BW_PASSWORD'] = master

        status = self.status()
        if status['template']['status'] != 'unauthenticated':
            self.__exec_cmd(['logout'])
        if status['template']['serverUrl'] != self._vault_url:
            self.__exec_cmd(['config', 'server', self._vault_url])

        success, response = self.__exec_cmd(['login', login, master])
        if not success:
            raise ConnectionError(response['message'])
        self.__session = response['raw']

    def __exec_cmd(self, cmd: list, env: dict = None) -> Tuple[bool, dict]:
        command = self._base_cmd + cmd
        exec_env = self.__prepare_env(env)
        p = subprocess.run(
            command, env=exec_env, capture_output=True, text=True
        )
        try:
            response = json.loads(p.stdout)
            if response['success']:
                return True, response['data']
            return False, {'message': response['message']}
        except json.JSONDecodeError:
            return False, {'message': p.stderr}

    def status(self) -> dict:
        success, status = self.__exec_cmd(['status'])
        if success:
            return status
        raise ConnectionError(status['message'])

    def unlock(self) -> None:
        cmd = ['unlock', '--passwordenv', 'BW_PASSWORD']
        env = {'BW_PASSWORD': os.environ['BW_PASSWORD']}
        success, response = self.__exec_cmd(cmd, env=env)
        if success:
            self.__session = response['raw']
        else:
            raise ConnectionError(response['message'])

    def find_by_url(self, url: str) -> Optional[BitwardenCredential]:
        if self.status()['template']['status'] == 'locked':
            self.unlock()
        cmd = ['list', 'items', '--url', url]
        env = {'BW_SESSION': self.__session}
        success, response = self.__exec_cmd(cmd, env=env)
        if not success:
            raise ConnectionError(response['message'])
        data = response['data']
        return BitwardenCredential(data[0]) if len(data) > 0 else None


class BitwardenKeyring(KeyringBackend):
    def __init__(self, login: str, password: str = None, **kwargs):
        super().__init__()
        self._client = BitwardenClient(login, password, **kwargs)

    @properties.classproperty
    @classmethod
    def priority(cls):
        if shutil.which('bw') is None:
            raise RuntimeError('Bitwarden client not found (bw)')
        return 1

    def get_password(self, service: str, username: str) -> Optional[str]:
        cred = self.get_credential(service, username)
        if cred is not None:
            return cred.password
        return None

    def get_credential(self, service: str, username: Optional[str]) \
            -> Optional[Credential]:
        return self._client.find_by_url(service)

    def set_password(self, service: str, username: str, password: str) -> None:
        raise PasswordSetError('Not supported')

    def delete_password(self, service: str, username: str) -> None:
        raise PasswordDeleteError('Not supported')
