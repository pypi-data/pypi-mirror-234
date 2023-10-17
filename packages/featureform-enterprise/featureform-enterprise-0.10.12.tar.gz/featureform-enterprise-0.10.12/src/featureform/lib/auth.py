import base64
import hashlib
import os
import threading
from abc import ABC, abstractmethod
from typing import Optional

import featureform as ff
import requests
from flask import Flask, request
from typeguard import typechecked
from werkzeug.serving import make_server


@typechecked
class AuthConfig(ABC):
    @abstractmethod
    def get_authorization_endpoint(self, redirect_uri: str, code_challenge: str) -> str:
        pass

    @abstractmethod
    def get_token_exchange_endpoint(self) -> str:
        pass


@typechecked
class OktaAuthConfig(AuthConfig):
    def __init__(
        self, domain: str, authorization_server_id: str, client_id: str
    ) -> None:
        self.domain = domain
        self.authorization_server_id = authorization_server_id
        self.client_id = client_id

    def get_authorization_endpoint(self, redirect_uri: str, code_challenge: str) -> str:
        return (
            f"https://{self.domain}/oauth2/{self.authorization_server_id}/v1/authorize?client_id={self.client_id}"
            f"&response_type=code&scope=openid&redirect_uri={redirect_uri}&state=random_state"
            f"&code_challenge_method=S256&code_challenge={code_challenge}"
        )

    def get_token_exchange_endpoint(self) -> str:
        return f"https://{self.domain}/oauth2/{self.authorization_server_id}/v1/token"


@typechecked
class AuthService(ABC):
    def __init__(self, auth_config) -> None:
        self._auth_config = auth_config

    @abstractmethod
    def authenticate(self) -> None:
        pass

    @abstractmethod
    def get_access_token(self) -> Optional[str]:
        pass

    @abstractmethod
    def clear_access_token(self) -> None:
        pass


@typechecked
class PassThroughService(AuthService):
    def authenticate(self) -> None:
        pass

    def get_access_token(self) -> Optional[str]:
        pass

    def clear_access_token(self) -> None:
        pass


@typechecked
class OktaOAuth2PKCE(AuthService):
    def __init__(self, auth_config: OktaAuthConfig) -> None:
        super().__init__(auth_config)
        # up casts the instance in this class to OktaAuthConfig
        self._auth_config: OktaAuthConfig = auth_config
        self.redirect_uri = "http://localhost:9080/authorization-code/callback"
        self._access_token = None
        self._code_verifier = None
        self._callback_server = None
        self._callback_server_thread = None
        self._callback_flask_app = Flask(__name__)
        self._auth_completed = threading.Event()

        @self._callback_flask_app.route("/authorization-code/callback")
        def callback():
            auth_code = request.args.get("code")
            threading.Thread(
                target=self._exchange_code_for_token, args=(auth_code,)
            ).start()
            return "Authentication successful! You can close this window."

    def authenticate(self) -> None:
        self._code_verifier = self._create_code_verifier()
        code_challenge = self._create_code_challenge(self._code_verifier)
        auth_url = self._auth_config.get_authorization_endpoint(
            self.redirect_uri, code_challenge
        )
        print(f"Please visit the following URL to authenticate: {auth_url}")
        self._callback_server_thread = threading.Thread(
            target=self._start_callback_server
        )
        self._callback_server_thread.start()
        self._auth_completed.wait()

    def get_access_token(self) -> Optional[str]:
        return self._access_token

    def clear_access_token(self) -> None:
        self._auth_completed.clear()
        self._access_token = None

    @staticmethod
    def _create_code_verifier():
        token = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
        return token.rstrip("=")

    @staticmethod
    def _create_code_challenge(verifier):
        m = hashlib.sha256()
        m.update(verifier.encode("utf-8"))
        challenge = base64.urlsafe_b64encode(m.digest()).decode("utf-8")
        return challenge.rstrip("=")

    def _exchange_code_for_token(self, auth_code):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        data = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": self.redirect_uri,
            "client_id": self._auth_config.client_id,
            "code_verifier": self._code_verifier,
        }
        try:
            response = requests.post(
                self._auth_config.get_token_exchange_endpoint(),
                headers=headers,
                data=data,
            )
            if response.status_code == 200:
                print("Authentication Succeeded!")
                self._access_token = response.json().get("access_token")
                self._auth_completed.set()
            else:
                raise Exception("Authentication Failed.")
        finally:
            self._stop_callback_server()

    def _start_callback_server(self):
        self._callback_server = make_server("127.0.0.1", 9080, self._callback_flask_app)
        self._callback_server.serve_forever()

    def _stop_callback_server(self):
        if self._callback_server:
            self._callback_server.shutdown()


@typechecked
class OktaOAuth2ClientCredentials(AuthService):
    def __init__(self, auth_config) -> None:
        super().__init__(auth_config)
        self._access_token = None

    def authenticate(self) -> None:
        client_id = os.environ.get("FF_OAUTH_CLIENT_ID")
        client_secret = os.environ.get("FF_OAUTH_CLIENT_SECRET")
        if not client_id or not client_secret:
            print("No client credentials found in Environment")
            return None
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        response = requests.post(
            self._auth_config.get_token_exchange_endpoint(), headers=headers, data=data
        )
        self._access_token = (
            response.json().get("access_token") if response.status_code == 200 else None
        )
        if self._access_token:
            print("Authentication Succeeded!")
        else:
            print("Failed to authenticate with client credentials")

    def get_access_token(self) -> Optional[str]:
        return self._access_token

    def clear_access_token(self) -> None:
        self._access_token = None


@typechecked
class AuthenticationManagerImpl:
    TOKEN_FILENAME = "access_token.txt"

    def __init__(self) -> None:
        self._access_token = None
        self._auth_config = None
        self._services = []
        feature_form_dir = os.environ.get("FEATUREFORM_DIR", ".featureform")
        self.auth_dir = os.path.join(feature_form_dir, "auth")
        os.makedirs(self.auth_dir, exist_ok=True)
        self.token_filepath = os.path.join(self.auth_dir, self.TOKEN_FILENAME)

    def _write_token_to_file(self, token: str):
        with open(self.token_filepath, "w") as f:
            f.write(token)
        os.chmod(self.token_filepath, 0o600)

    def _read_token_from_file(self) -> Optional[str]:
        if os.path.exists(self.token_filepath):
            with open(self.token_filepath, "r") as f:
                return f.read().strip()
        return None

    def delete_expired_token(self):
        self._access_token = None
        for service in self._services:
            service.clear_access_token()
        feature_form_dir = os.environ.get("FEATUREFORM_DIR", ".featureform")
        auth_dir = os.path.join(feature_form_dir, "auth")
        token_filepath = os.path.join(
            auth_dir, AuthenticationManagerImpl.TOKEN_FILENAME
        )
        if os.path.exists(token_filepath):
            os.remove(token_filepath)

    def get_access_token_or_authenticate(self, insecure, host) -> Optional[str]:
        if not self._access_token:
            self._access_token = self._read_token_from_file()
            if not self._access_token:
                if not self._services:
                    self._auth_config = self._load_auth_config(insecure, host)
                    if self._auth_config is not None:
                        self._services = [
                            OktaOAuth2ClientCredentials(self._auth_config),
                            OktaOAuth2PKCE(self._auth_config),
                        ]
                    else:
                        self._services = [PassThroughService(self._auth_config)]

                for service in self._services:
                    service.authenticate()
                    token = service.get_access_token()
                    if token:
                        self._access_token = token
                        self._write_token_to_file(token)
                        break
        return self._access_token

    @staticmethod
    def _load_auth_config(insecure, host) -> Optional[OktaAuthConfig]:
        config = ff.Client(insecure=insecure, host=host).get_auth_config()
        if config.WhichOneof("config") == "okta":
            okta_config = config.okta
            return OktaAuthConfig(
                domain=okta_config.domain,
                authorization_server_id=okta_config.authorization_server_id,
                client_id=okta_config.client_id,
            )
        elif config.WhichOneof("config") == "pass_through":
            return None


singleton = AuthenticationManagerImpl()
