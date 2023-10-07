import os
from unittest.mock import Mock, patch
from src.argus_enterprise_api import ArgusClient
import unittest


def dummy_get_access_token(self):
    self._access_token = "dummy_token"


class TestArgusClient(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cert_path = os.path.join(current_dir, "test_cert.pkcs12")
        with patch.object(ArgusClient, "_get_access_token", new=dummy_get_access_token):
            self.argus_client = ArgusClient(
                client_key="client_key",
                client_secret="client_secret",
                cert_path=cert_path,
                cert_pwd="password",
                email="email@example.com",
                env_id="env_id",
                version="5.0",
            )

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            ArgusClient(
                client_key="client_key",
                client_secret="client_secret",
                cert_path="cert_path.p12",
                cert_pwd="cert_pwd",
                email="invalidemail",
                env_id="env_id",
                version="5.0",
            )

    def test_invalid_version(self):
        with self.assertRaises(ValueError):
            ArgusClient(
                client_key="client_key",
                client_secret="client_secret",
                cert_path="cert_path.p12",
                cert_pwd="cert_pwd",
                email="email@example.com",
                env_id="env_id",
                version="invalid_version",
            )

    @patch("requests.post")
    def test_get_access_token(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "token_value",
            "expires_in": 3600,
        }
        mock_response.ok = True
        mock_post.return_value = mock_response

        self.argus_client._get_access_token()
        self.assertEqual(self.argus_client._access_token, "token_value")


if __name__ == "__main__":
    unittest.main()
