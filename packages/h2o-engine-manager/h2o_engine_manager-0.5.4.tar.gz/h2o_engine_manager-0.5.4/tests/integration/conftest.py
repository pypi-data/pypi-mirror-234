import os

import pytest

import h2o_engine_manager
from h2o_engine_manager.clients.dai_engine_constraint.client import (
    DAIEngineConstraintSetClient,
)
from h2o_engine_manager.clients.engine.client import EngineClient
from h2o_engine_manager.clients.h2o_engine_constraint.client import (
    H2OEngineConstraintSetClient,
)
from h2o_engine_manager.clients.internal_dai_version.client import (
    InternalDAIVersionClient,
)
from h2o_engine_manager.clients.internal_h2o_version.client import (
    InternalH2OVersionClient,
)

# Kubernetes cache needs to take some time to detect changes in k8s server.
CACHE_SYNC_SECONDS = 0.2

# To have control over the provisioned test resources, a workspace with related DAISetup is used.
DAI_SETUP_WORKSPACE = "dai-setup"
DAI_LIFECYCLE_WORKSPACE = "dai-lifecycle"
DAI_CONNECT_WORKSPACE = "dai-connect"

H2O_SETUP_WORKSPACE = "h2o-setup"

# Non-mocked version of DAI.
NON_MOCKED_DAI_VERSION = "1.10.4"


@pytest.fixture(scope="session")
def clients():
    return h2o_engine_manager.login_custom(
        endpoint=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
        refresh_token=os.getenv("PLATFORM_TOKEN_USER"),
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )


@pytest.fixture(scope="session")
def admin_clients():
    return h2o_engine_manager.login_custom(
        endpoint=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
        refresh_token=os.getenv("PLATFORM_TOKEN_ADMIN"),
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )


@pytest.fixture(scope="session")
def super_admin_clients():
    return h2o_engine_manager.login_custom(
        endpoint=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
        refresh_token=os.getenv("PLATFORM_TOKEN_SUPER_ADMIN"),
        issuer_url=os.getenv("PLATFORM_OIDC_URL"),
        client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )


@pytest.fixture(scope="session")
def dai_client(clients):
    return clients.dai_engine_client


@pytest.fixture(scope="session")
def dai_admin_client(admin_clients):
    return admin_clients.dai_engine_client


@pytest.fixture(scope="session")
def h2o_engine_client(clients):
    return clients.h2o_engine_client


@pytest.fixture(scope="session")
def engine_client():
    return EngineClient(
        url=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
        platform_token=os.getenv("PLATFORM_TOKEN_USER"),
        platform_oidc_url=os.getenv("PLATFORM_OIDC_URL"),
        platform_oidc_client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )


@pytest.fixture(scope="session")
def dai_engine_constraint_set_client():
    return DAIEngineConstraintSetClient(
        url=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
        platform_token=os.getenv("PLATFORM_TOKEN_USER"),
        platform_oidc_url=os.getenv("PLATFORM_OIDC_URL"),
        platform_oidc_client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )


@pytest.fixture(scope="session")
def h2o_engine_constraint_set_client():
    return H2OEngineConstraintSetClient(
        url=os.getenv("AIEM_SCHEME") + "://" + os.getenv("AIEM_HOST"),
        platform_token=os.getenv("PLATFORM_TOKEN_USER"),
        platform_oidc_url=os.getenv("PLATFORM_OIDC_URL"),
        platform_oidc_client_id=os.getenv("PLATFORM_OIDC_CLIENT_ID"),
    )


@pytest.fixture(scope="session")
def dai_profile_client(super_admin_clients):
    return super_admin_clients.dai_profile_client


@pytest.fixture(scope="session")
def adjusted_dai_profile_client(dai_client):
    return dai_client.adjusted_profile_client


@pytest.fixture(scope="function")
def dai_profile_cleanup_after(dai_profile_client):
    yield

    profiles = dai_profile_client.list_all_profiles()
    for p in profiles:
        dai_profile_client.delete_profile(profile_id=p.dai_profile_id)


@pytest.fixture(scope="session")
def websocket_base_url() -> str:
    scheme = os.getenv("AIEM_SCHEME")
    host = os.getenv("AIEM_HOST")

    if scheme == "http":
        return f"ws://{host}"
    elif scheme == "https":
        return f"wss://{host}"

    raise ValueError(f"AIEM_SCHEME must be either http or https, got scheme: {scheme}")


@pytest.fixture(scope="session")
def internal_dai_version_client(super_admin_clients):
    return super_admin_clients.internal_dai_version_client


@pytest.fixture(scope="session")
def internal_dai_version_client_standard_user(clients) -> InternalDAIVersionClient:
    return clients.internal_dai_version_client


@pytest.fixture(scope="session")
def internal_dai_version_client_admin(admin_clients) -> InternalDAIVersionClient:
    return admin_clients.internal_dai_version_client


@pytest.fixture(scope="function")
def internal_dai_versions_cleanup_after(internal_dai_version_client):
    yield

    versions = internal_dai_version_client.list_all_versions()
    for v in versions:
        internal_dai_version_client.delete_version(internal_dai_version_id=v.internal_dai_version_id)


@pytest.fixture(scope="session")
def internal_h2o_version_client(super_admin_clients):
    return super_admin_clients.internal_h2o_version_client


@pytest.fixture(scope="session")
def internal_h2o_version_client_standard_user(clients) -> InternalH2OVersionClient:
    return clients.internal_h2o_version_client


@pytest.fixture(scope="session")
def internal_h2o_version_client_admin(admin_clients) -> InternalH2OVersionClient:
    return admin_clients.internal_h2o_version_client


@pytest.fixture(scope="function")
def internal_h2o_versions_cleanup_after(internal_h2o_version_client):
    yield

    versions = internal_h2o_version_client.list_all_versions()
    for v in versions:
        internal_h2o_version_client.delete_version(internal_h2o_version_id=v.internal_h2o_version_id)
