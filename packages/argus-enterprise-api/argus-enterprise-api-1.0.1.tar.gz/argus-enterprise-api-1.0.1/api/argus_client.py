from .blueprints import Workspace, ModelManagement

from validate_email_address import validate_email
import requests
import json
import jwt
import time
import base64
from random import randint
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import pkcs12


class ArgusClient:
    """
    ArgusClient: A Python client for interacting with the Argus API by Altus Group.

    This client is built to interface with Argus API versions 3.0, 4.0, and 5.0,
    and it relies on Swagger for API specification and dynamic method generation.

    Attributes:
      client_key (str): Client key for API authentication.
      client_secret (str): Client secret for API authentication.
      cert_path (str): Path to the PKCS12 certificate file.
      cert_pwd (str): Password for the PKCS12 certificate.
      email (str): User's email address that has been granted in Argus Cloud.
      env_id (str): Environment ID.
      version (str): API version to be used. Must be one of ['3.0', '4.0', '5.0'].

    Classes:
        workspaces: Provides methods to interact with the Workspaces API.
        model_management: Provides methods to interact with the Model Management API.

    Documentation:
        For more technical details, refer to https://cloud.altusplatform.com/help/index.htm
        Workspaces API Swagger: https://cloud.altusplatform.com/help/WorkspaceApi-5_0.html (replace 5_0 with your required version)
        Model Management API Swagger: https://cloud.altusplatform.com/help/ModelManagementApi-5_0.html (replace 5_0 with your required version)

    Example:
      client = ArgusClient(
        client_key="your_key",
        client_secret="your_secret",
        cert_path="/path/to/cert.p12",
        cert_pwd="your_password",
        email="your@email.com",
        env_id="your_env_id",
        version="your_version"
      )
    """

    _VALID_VERSIONS = {"3.0", "4.0", "5.0"}
    _ALG = "RS256"
    _TOKEN_URL = "https://identity.altusplatform.com/oauth2/token"
    _TOKEN_EXP_SEC = 3600
    _TOKEN_REQUEST_DETAILS = (
        "grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion={token}"
    )

    def __init__(
        self,
        client_key,
        client_secret,
        cert_path,
        cert_pwd,
        email,
        env_id,
        version="5.0",
    ):
        if not validate_email(email):
            raise ValueError("Invalid email address")

        if version not in self._VALID_VERSIONS:
            raise ValueError(
                f"Invalid version specified. Must be one of {self._VALID_VERSIONS}"
            )

        self._client_key = client_key
        self._client_secret = client_secret
        self._cert_path = cert_path
        self._cert_pwd = cert_pwd
        self.email = email
        self._env_id = env_id
        self.version = version
        self._access_token = None
        self.token_expiry = None

        self._get_access_token()

        self.workspace = Workspace(self)
        self.model_management = ModelManagement(self)

    def _generate_jwt_token(self):
        if not self._cert_path.lower().endswith((".p12", ".pfx", ".pkcs12")):
            raise ValueError(
                f"The certificate file must be a PKCS12 file (.p12, .pfx, or .pkcs12). Provided: '{self._cert_path}'"
            )

        try:
            with open(self._cert_path, "rb") as cert_file:
                pkcs12_data = cert_file.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"The certificate file '{self._cert_path}' was not found."
            )
        except PermissionError:
            raise PermissionError(
                f"Permission denied when trying to read '{self._cert_path}'."
            )

        password_bytes = self._cert_pwd.encode()
        private_key, certificate, _ = pkcs12.load_key_and_certificates(
            pkcs12_data, password_bytes
        )
        private_key_value = private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )

        kid = certificate.fingerprint(hashes.SHA1()).hex()

        current_time = int(time.time())
        claims = {
            "sub": self.email,
            "aud": self._TOKEN_URL,
            "iss": "JWT_IDP",
            "exp": current_time + self._TOKEN_EXP_SEC,
            "iat": current_time,
            "jti": str(randint(0, 9999)),
        }

        headers = {"typ": "JWT", "alg": self._ALG, "kid": kid}

        jwt_token = jwt.encode(claims, private_key_value, self._ALG, headers)
        return jwt_token

    def _get_access_token(self):
        token = self._generate_jwt_token()
        encoded_credentials = base64.b64encode(
            (f"{self._client_key}:{self._client_secret}").encode()
        ).decode()
        request_data_str = self._TOKEN_REQUEST_DETAILS.format(token=token)
        data = bytes(request_data_str, "ascii")

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(url=self._TOKEN_URL, data=data, headers=headers)

        if response.ok:
            response_json = json.loads(str(response.json()).replace("'", '"'))
            self.token_expiry = time.time() + response_json["expires_in"]
            self._access_token = response_json["access_token"]
        else:
            raise requests.RequestException(response.json())

    def _get_base_headers(self):
        if not self._access_token or (
            self.token_expiry and time.time() > self.token_expiry
        ):
            self._get_access_token()

        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "Environment_Id": self._env_id,
            "Content-Type": "application/json",
        }

        return headers
