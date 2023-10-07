from unittest.mock import patch, Mock

import pytest

from featureform.lib import auth, OktaAuthConfig, OktaOAuth2PKCE, OktaOAuth2ClientCredentials


def test_okta_auth_config():
    config = OktaAuthConfig("domain.com", "server", "client123")
    expected_endpoint = "https://domain.com/oauth2/server/v1/authorize?client_id=client123&response_type=code&scope=openid&redirect_uri=some_uri&state=random_state&code_challenge_method=S256&code_challenge=some_challenge"
    assert config.get_authorization_endpoint("some_uri", "some_challenge") == expected_endpoint
    assert config.get_token_exchange_endpoint() == "https://domain.com/oauth2/server/v1/token"


def test_code_verifier_creation():
    config = OktaAuthConfig("domain.com", "server", "client123")
    service = OktaOAuth2PKCE(config)
    verifier = service._create_code_verifier()
    assert len(verifier) == 54  # This assumes a 40-byte token as input


def test_code_challenge_creation():
    config = OktaAuthConfig("domain.com", "server", "client123")
    service = OktaOAuth2PKCE(config)
    verifier = "some_verifier"
    challenge = service._create_code_challenge(verifier)
    assert len(challenge) <= 44  # Base64 url-safe encoded SHA256


@patch("requests.post")
def test_exchange_code_for_token_success(mock_post):
    config = OktaAuthConfig("domain.com", "server", "client123")
    service = OktaOAuth2PKCE(config)

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "access_token": "some_access_token"
    }
    mock_post.return_value = mock_response

    service._exchange_code_for_token("some_auth_code")
    assert service.get_access_token() == "some_access_token"


@patch("requests.post")
def test_exchange_code_for_token_fail(mock_post):
    config = OktaAuthConfig("domain.com", "server", "client123")
    service = OktaOAuth2PKCE(config)

    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {}
    mock_post.return_value = mock_response

    with pytest.raises(Exception) as e:
        service._exchange_code_for_token("some_auth_code")
    assert str(e.value) == "Authentication Failed."
    assert service.get_access_token() is None


@patch("requests.post")
@patch("os.environ")
def test_client_credentials_success(mock_environ, mock_post):
    mock_environ.get.side_effect = ["client_id", "client_secret"]
    config = OktaAuthConfig("domain.com", "server", "client123")
    service = OktaOAuth2ClientCredentials(config)

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "access_token": "some_access_token"
    }
    mock_post.return_value = mock_response

    service.authenticate()
    assert service.get_access_token() == "some_access_token"


@patch("requests.post")
@patch("os.environ")
def test_client_credentials_fail(mock_environ, mock_post):
    mock_environ.get.side_effect = [None, None]
    config = OktaAuthConfig("domain.com", "server", "client123")
    service = OktaOAuth2ClientCredentials(config)

    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {}
    mock_post.return_value = mock_response

    service.authenticate()
    assert service.get_access_token() is None


@patch.object(OktaOAuth2PKCE, 'authenticate')
@patch.object(OktaOAuth2PKCE, 'get_access_token', return_value="token")
@patch.object(auth.singleton, '_load_auth_config', return_value=OktaAuthConfig(
    domain="",
    authorization_server_id="",
    client_id="",
))
def test_authentication_manager_success(mock_get_access_token, mock_authenticate, mocked_load):
    assert auth.singleton._access_token is None
    token = auth.singleton.get_access_token_or_authenticate(insecure=True)
    assert token == "token"
    auth.singleton._access_token = "override_with_cache_token"
    token_cached = auth.singleton.get_access_token_or_authenticate(insecure=True)
    assert token_cached == "override_with_cache_token"


# Demo program

def execute_dummy_method():
    print("Executing dummy method...")


if __name__ == "__main__":
    access_token = None

    while True:
        print("\nChoose an action:")
        print("1. Execute dummy method")
        print("2. Exit")
        choice = input("> ")

        if choice == '1':
            if not access_token:
                access_token = auth.singleton.get_access_token_or_authenticate(insecure=True)
                if not access_token:
                    print("Failed to authenticate.")
                    continue
            execute_dummy_method()

        elif choice == '2':
            break
