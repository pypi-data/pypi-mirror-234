from drb.keyring.bitwarden import (
    BitwardenCredential, BitwardenClient, BitwardenKeyring
)
from unittest.mock import patch
from subprocess import CompletedProcess
from keyring.errors import PasswordDeleteError, PasswordSetError
import json
import os
import unittest


class TestBitwardenCredentials(unittest.TestCase):
    default_data = None

    @classmethod
    def setUpClass(cls) -> None:
        resource_dir = os.path.join(
            os.path.dirname(__file__),
            'resources/keyring/bitwarden'
        )
        with open(os.path.join(resource_dir, 'list.json'), 'r') as file:
            data = json.load(file)
            cls.default_data = data['data']['data'][0]

    def test_username(self):
        cred = BitwardenCredential(self.default_data)
        self.assertEqual('my-secret-username', cred.username)

    def test_password(self):
        cred = BitwardenCredential(self.default_data)
        self.assertEqual('my-secret-password', cred.password)

    def test_in(self):
        cred = BitwardenCredential(self.default_data)
        self.assertTrue('uid' in cred)
        self.assertFalse('foobar' in cred)

    def test_getitem(self):
        cred = BitwardenCredential(self.default_data)
        self.assertEqual('uid-value', cred['uid'])

        with self.assertRaises(KeyError):
            cred['foobar']

    def test_get(self):
        cred = BitwardenCredential(self.default_data)
        self.assertEqual('uid-value', cred.get('uid'))
        self.assertEqual('key-api-value', cred.get('key-api'))
        self.assertIsNone(cred.get('foobar'))


class TestBitwardenClient(unittest.TestCase):
    commands = None

    @classmethod
    def setUpClass(cls) -> None:
        resource_dir = os.path.join(
            os.path.dirname(__file__),
            'resources/keyring/bitwarden'
        )
        cls.commands = {
            'config': os.path.join(resource_dir, 'config.json'),
            'list': os.path.join(resource_dir, 'list.json'),
            'login': os.path.join(resource_dir, 'login_unlock.json'),
            'logout': os.path.join(resource_dir, 'logout.json'),
            'status': os.path.join(resource_dir, 'status.json'),
            'unlock': os.path.join(resource_dir, 'login_unlock.json'),
        }

    @classmethod
    def subprocess_run_side_effect(cls, *args, **kwargs):
        command = args[0][4]
        try:
            with open(cls.commands[command], 'r') as file:
                return CompletedProcess(
                    args, returncode=0, stdout=file.read().encode())
        except KeyError:
            m = f'{{"success": false, "message": "unknown command {command}"}}'
            return CompletedProcess(args, returncode=1, stdout=m)

    @classmethod
    def subprocess_run_side_effect_error(cls, *args, **kwargs):
        message = '{"success": false, "message": "expected error"}'
        return CompletedProcess(args, returncode=1, stdout=message)

    @patch("drb.keyring.bitwarden.bitwarden.subprocess.run")
    def test_status(self, mock_run):
        mock_run.side_effect = self.subprocess_run_side_effect
        client = BitwardenClient('username', 'master-secret')
        with open(self.commands['status']) as file:
            self.assertEqual(json.load(file)['data'], client.status())

        mock_run.side_effect = self.subprocess_run_side_effect_error
        with self.assertRaises(ConnectionError):
            client.status()

    @patch("drb.keyring.bitwarden.bitwarden.subprocess.run")
    def test_unlock(self, mock_run):
        secret = 'master-secret'
        mock_run.side_effect = self.subprocess_run_side_effect
        client = BitwardenClient('username', secret)
        client.unlock()
        expected_args = [
            'bw',
            '--nointeraction',
            '--response',
            '--pretty',
            'unlock',
            '--passwordenv',
            'BW_PASSWORD',
        ]
        expected_kwargs = os.environ.copy()
        expected_kwargs['BW_PASSWORD'] = secret
        mock_run.assert_called_with(
            expected_args,
            env=expected_kwargs,
            capture_output=True,
            text=True
        )

        mock_run.side_effect = self.subprocess_run_side_effect_error
        with self.assertRaises(ConnectionError):
            client.unlock()

    @patch("drb.keyring.bitwarden.bitwarden.subprocess.run")
    def test_find_by_url(self, mock_run):
        mock_run.side_effect = self.subprocess_run_side_effect
        client = BitwardenClient('username', 'master-secret')
        credentials = client.find_by_url('cds.climate.copernicus.eu')
        self.assertIsNotNone(credentials)
        self.assertEqual('my-secret-username', credentials.username)
        self.assertEqual('my-secret-password', credentials.password)
        self.assertEqual('uid-value', credentials.get('uid'))
        self.assertEqual('key-api-value', credentials.get('key-api'))


class TestBitwardenKeyring(unittest.TestCase):
    data = None

    @classmethod
    def setUpClass(cls) -> None:
        resource_dir = os.path.join(
            os.path.dirname(__file__), 'resources/keyring/bitwarden')
        with open(os.path.join(resource_dir, 'list.json')) as file:
            cls.data = json.load(file)['data']['data'][0]

    @patch("drb.keyring.bitwarden.bitwarden.shutil")
    def test_priority(self, shutil):
        shutil.which.return_value = 'somewhere'
        self.assertEqual(1, BitwardenKeyring.priority)

        shutil.which.return_value = None
        with self.assertRaises(RuntimeError):
            BitwardenKeyring.priority

    @patch("drb.keyring.bitwarden.bitwarden.BitwardenClient")
    def test_get_password(self, client):
        credential = BitwardenCredential(self.data)
        client.find_by_url.return_value = credential
        ring = BitwardenKeyring('username', 'password')
        ring._client = client
        self.assertEqual('my-secret-password', ring.get_password('svc', 'usr'))

    @patch("drb.keyring.bitwarden.bitwarden.BitwardenClient")
    def test_get_credentials(self, client):
        credential = BitwardenCredential(self.data)
        client.find_by_url.return_value = credential
        ring = BitwardenKeyring('username', 'password')
        ring._client = client
        self.assertEqual(credential, ring.get_credential('svc', 'usr'))

    @patch("drb.keyring.bitwarden.bitwarden.BitwardenClient")
    def test_set_password(self, client):
        ring = BitwardenKeyring('username', 'password')
        with self.assertRaises(PasswordSetError):
            ring.set_password('svc', 'usr', 'pwd')

    @patch("drb.keyring.bitwarden.bitwarden.BitwardenClient")
    def test_delete_password(self, client):
        ring = BitwardenKeyring('username', 'password')
        with self.assertRaises(PasswordDeleteError):
            ring.delete_password('svc', 'usr')
