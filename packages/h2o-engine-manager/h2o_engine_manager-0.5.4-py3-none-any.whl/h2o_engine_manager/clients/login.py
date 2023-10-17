from typing import Callable
from typing import Optional
from urllib.parse import urljoin

import requests

from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.connection_config import discover_platform_connection
from h2o_engine_manager.clients.connection_config import get_connection
from h2o_engine_manager.clients.dai_engine.dai_engine_client import DAIEngineClient
from h2o_engine_manager.clients.dai_profile.client import DAIProfileClient
from h2o_engine_manager.clients.h2o_engine.client import H2OEngineClient
from h2o_engine_manager.clients.internal_dai_version.client import (
    InternalDAIVersionClient,
)
from h2o_engine_manager.clients.internal_h2o_version.client import (
    InternalH2OVersionClient,
)


class Clients:
    def __init__(
        self,
        dai_engine_client: DAIEngineClient,
        h2o_engine_client: H2OEngineClient,
        dai_profile_client: DAIProfileClient,
        internal_dai_version_client: InternalDAIVersionClient,
        internal_h2o_version_client: InternalH2OVersionClient,
    ) -> None:
        self.dai_engine_client = dai_engine_client
        self.h2o_engine_client = h2o_engine_client
        self.dai_profile_client = dai_profile_client
        self.internal_dai_version_client = internal_dai_version_client
        self.internal_h2o_version_client = internal_h2o_version_client


def login(
    environment: Optional[str] = None,
    token_provider: Callable[[], str] = None,
    platform_token: Optional[str] = None,
    default_workspace_id: str = "default",
    config_path: str = None,
    verify_ssl: bool = True,
    ssl_ca_cert: Optional[str] = None,
) -> Clients:
    """Initializes AI Engine Manager clients for H2O AI Cloud.

    All arguments are optional. Configuration-less login is dependent on having the H2O CLI configured.
    See: https://docs.h2o.ai/h2o-ai-cloud/developerguide/cli#platform-token
    The Discovery Service is used to discover the Engine Manager service endpoint.
    See: https://pypi.org/project/h2o-cloud-discovery/

    Args:
        environment (str, optional): The H2O Cloud environment URL to use (e.g. https://cloud.h2o.ai).
            If left empty, the environment will be read from the H2O CLI configuration or environmental variables.
            Then, h2o-cloud-discovery will be used to discover the Engine Manager service endpoint.
        token_provider (Callable[[], str], optional) = A callable function providing access token.
            Takes priority over platform_token argument.
        platform_token (str, optional): H2O Platform Token.
            If neither 'token_provider' nor 'platform_token' is provided the platform token will be read
            from the H2O CLI configuration.
        default_workspace_id (str, optional): The default workspace ID which will client use to manipulate with
            resources. Defaults to `default`.
        config_path: (str, optional): Path to the H2O AI Cloud configuration file.
            Defaults to '~/.h2oai/h2o-cli-config.toml'.
        verify_ssl: Set to False to disable SSL certificate verification.
        ssl_ca_cert: Path to a CA cert bundle with certificates of trusted CAs.

    Raises:
        FileNotFoundError: When the H2O CLI configuration file is needed but cannot be found.
        TomlDecodeError: When the H2O CLI configuration file is needed but cannot be processed.
        LookupError: When the service endpoint cannot be discovered.
        ConnectionError: When a communication with server failed.
    """

    cfg = discover_platform_connection(
        environment_url=environment,
        platform_token=platform_token,
        token_provider=token_provider,
        config_path=config_path,
    )

    return __init_clients(
        cfg=cfg, default_workspace_id=default_workspace_id, verify_ssl=verify_ssl, ssl_ca_cert=ssl_ca_cert,
    )


def login_custom(
    endpoint: str,
    refresh_token: str,
    issuer_url: str,
    client_id: str,
    client_secret: Optional[str] = None,
    default_workspace_id: str = "default",
    verify_ssl: bool = True,
    ssl_ca_cert: Optional[str] = None,
) -> Clients:
    """Initializes AI Engine Manager clients.

    Args:
        endpoint (str): The Engine Manager service endpoint URL (e.g. https://enginemanager.cloud.h2o.ai).
        refresh_token (str): The OIDC refresh token.
        issuer_url (str): The OIDC issuer URL.
        client_id (str): The OIDC Client ID that issued the 'refresh_token'.
        client_secret (str, optional): Optional OIDC Client Secret that issued the 'refresh_token'. Defaults to None.
        default_workspace_id (str, optional): The default workspace ID which will client use to manipulate with
            resources. Defaults to `default`.
        verify_ssl: Set to False to disable SSL certificate verification.
        ssl_ca_cert: Path to a CA cert bundle with certificates of trusted CAs.
    """
    # Remove trailing slash from the URL for the generated clients
    endpoint = endpoint.rstrip("/")
    cfg = get_connection(
        aiem_url=endpoint,
        refresh_token=refresh_token,
        issuer_url=issuer_url,
        client_id=client_id,
        client_secret=client_secret,
    )

    return __init_clients(
        cfg=cfg, default_workspace_id=default_workspace_id, verify_ssl=verify_ssl, ssl_ca_cert=ssl_ca_cert,
    )


def __init_clients(
    cfg: ConnectionConfig,
    default_workspace_id: str,
    verify_ssl: bool,
    ssl_ca_cert: str,
):
    # Verify that the server is reachable
    version_url = urljoin(cfg.aiem_url, "version")
    resp = requests.get(version_url)
    if not (200 <= resp.status_code <= 299):
        raise ConnectionError(
            f"Server is not reachable. Status code: {resp.status_code}, Response body: {resp.text}"
        )

    dai_engine_client = DAIEngineClient(
        connection_config=cfg, default_workspace_id=default_workspace_id, verify_ssl=verify_ssl,
        ssl_ca_cert=ssl_ca_cert,
    )
    h2o_engine_client = H2OEngineClient(
        connection_config=cfg, default_workspace_id=default_workspace_id, verify_ssl=verify_ssl,
        ssl_ca_cert=ssl_ca_cert,
    )
    dai_profile_client = DAIProfileClient(
        connection_config=cfg, verify_ssl=verify_ssl,
        ssl_ca_cert=ssl_ca_cert,
    )
    internal_dai_version_client = InternalDAIVersionClient(
        connection_config=cfg, verify_ssl=verify_ssl, ssl_ca_cert=ssl_ca_cert
    )
    internal_h2o_version_client = InternalH2OVersionClient(
        connection_config=cfg, verify_ssl=verify_ssl, ssl_ca_cert=ssl_ca_cert
    )
    return Clients(
        dai_engine_client=dai_engine_client,
        h2o_engine_client=h2o_engine_client,
        dai_profile_client=dai_profile_client,
        internal_dai_version_client=internal_dai_version_client,
        internal_h2o_version_client=internal_h2o_version_client,
    )
