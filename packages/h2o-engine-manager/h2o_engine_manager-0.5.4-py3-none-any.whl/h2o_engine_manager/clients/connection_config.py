import os
from typing import Callable
from typing import NamedTuple
from typing import Optional

import h2o_authn
import h2o_discovery

# Name of the platform client in the discovery response.
PLATFORM_CLIENT_NAME = "platform"
# Name of the AIEM service in the discovery response.
AIEM_SERVICE_NAME = "engine-manager"


class ConnectionConfig(NamedTuple):
    """Object holding connection configuration for the AIEM server."""

    aiem_url: str
    token_provider: Callable[[], str]


def get_connection(
    aiem_url: str,
    refresh_token: str,
    issuer_url: str,
    client_id: str,
    client_secret: Optional[str] = None,
) -> ConnectionConfig:
    """Creates ConnectionConfig object. Initializes and tests token provider."""

    # init token provider
    tp = h2o_authn.TokenProvider(
        issuer_url=issuer_url,
        refresh_token=refresh_token,
        client_id=client_id,
        client_secret=client_secret,
    )
    # test token refresh
    tp()

    return ConnectionConfig(aiem_url=aiem_url, token_provider=tp)


def discover_platform_connection(
        environment_url: Optional[str] = None,
        config_path: str = None,
        platform_token: Optional[str] = None,
        token_provider: Callable[[], str] = None,
) -> ConnectionConfig:
    """Creates ConnectionConfig object by discovering platform connection configuration using h2o_discovery.

    :param environment_url: Override for the URL of the environment passed to the discovery service.
    :param config_path: Override path to the h2o cli config file passed to the discovery service.
    :param platform_token: Platform token. If not provided, the token will be discovered.
    :param token_provider: Token provider. If not provided, the provider will be constructed from the discovered config.
    """
    # Discover the AIEM server URL
    d = h2o_discovery.discover(environment=environment_url, config_path=config_path)
    aiem_url = d.services.get(AIEM_SERVICE_NAME).uri
    if not aiem_url:
        raise ConnectionError("Unable to discover AIEM server URL connection value.")

    # If the token provider is provided, use it to construct the connection config.
    if token_provider is not None:
        # Test token refresh
        token_provider()
        return ConnectionConfig(aiem_url=aiem_url, token_provider=token_provider)

    # If the token provider is not provided, construct it from the discovered config.
    if not platform_token:
        platform_token = d.credentials[PLATFORM_CLIENT_NAME].refresh_token

    if not platform_token:
        raise ValueError(
            "Please set the 'platform_token' argument or configure the H2O CLI."
        )

    # Discover client id
    client_id = d.clients.get(PLATFORM_CLIENT_NAME).oauth2_client_id
    if not client_id:
        raise ConnectionError(
            "Unable to discover platform oauth2_client_id connection value."
        )

    tp = h2o_authn.TokenProvider(
        issuer_url=d.environment.issuer_url,
        client_id=client_id,
        refresh_token=platform_token,
    )
    # Test token refresh
    tp()

    return ConnectionConfig(aiem_url=aiem_url, token_provider=tp)
