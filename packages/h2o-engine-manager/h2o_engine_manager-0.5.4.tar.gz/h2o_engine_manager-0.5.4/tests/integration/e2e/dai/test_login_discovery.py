import os

import h2o_authn
import pytest
from requests.exceptions import ConnectionError

import h2o_engine_manager


def test_login_args_provided():
    h2o_engine_manager.login(
        environment=os.getenv("AIEM_DISCOVERY_URL"),
        platform_token=os.getenv("PLATFORM_TOKEN_USER"),
    )


def test_login_h2o_cli_config():
    h2o_engine_manager.login()


def test_login_token_provider():
    os.environ["H2O_CLOUD_ENVIRONMENT"] = os.getenv("AIEM_DISCOVERY_URL")

    tp = h2o_authn.TokenProvider(
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
        refresh_token=os.getenv("PLATFORM_TOKEN_USER"),
    )
    h2o_engine_manager.login(token_provider=tp)


def test_incorrect_url():
    with pytest.raises(ConnectionError):
        h2o_engine_manager.login_custom(
            endpoint="https://incorrect-url.com",
            refresh_token=os.getenv("PLATFORM_TOKEN_USER"),
            issuer_url=os.getenv("PLATFORM_OIDC_URL"),
            client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
        )
