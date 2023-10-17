import time

from h2o_engine_manager.clients.internal_h2o_version.client import (
    InternalH2OVersionClient,
)
from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_list_all(internal_h2o_version_client, internal_h2o_versions_cleanup_after):
    create_h2o_versions(internal_h2o_version_client)
    time.sleep(CACHE_SYNC_SECONDS)

    versions = internal_h2o_version_client.list_all_versions()

    assert len(versions) == 3

    assert versions[0].version == "3.40.0.6"
    assert versions[0].image == "h2o-3.40.0.6"
    assert len(versions[0].aliases) == 1
    assert versions[0].aliases[0] == "latest"

    assert versions[1].version == "3.40.0.5"
    assert versions[1].image == "h2o-3.40.0.5"
    assert len(versions[1].aliases) == 0

    assert versions[2].version == "3.40.0.4"
    assert versions[2].image == "h2o-3.40.0.4"
    assert len(versions[2].aliases) == 0


def test_list(internal_h2o_version_client, internal_h2o_versions_cleanup_after):
    create_h2o_versions(internal_h2o_version_client)
    time.sleep(CACHE_SYNC_SECONDS)

    response = internal_h2o_version_client.list_versions(page_size=2)
    versions = response.internal_h2o_versions

    assert len(versions) == 2
    assert response.total_size == 3
    assert response.next_page_token != ""

    assert versions[0].version == "3.40.0.6"
    assert versions[0].image == "h2o-3.40.0.6"
    assert len(versions[0].aliases) == 1
    assert versions[0].aliases[0] == "latest"

    assert versions[1].version == "3.40.0.5"
    assert versions[1].image == "h2o-3.40.0.5"
    assert len(versions[1].aliases) == 0

    response = internal_h2o_version_client.list_versions(page_size=100, page_token=response.next_page_token)
    versions = response.internal_h2o_versions

    assert len(versions) == 1
    assert response.total_size == 3
    assert response.next_page_token == ""

    assert versions[0].version == "3.40.0.4"
    assert versions[0].image == "h2o-3.40.0.4"


def create_h2o_versions(internal_h2o_version_client: InternalH2OVersionClient):
    internal_h2o_version_client.create_version(
        internal_h2o_version_id="3.40.0.4",
        image="h2o-3.40.0.4"
    )
    internal_h2o_version_client.create_version(
        internal_h2o_version_id="3.40.0.5",
        image="h2o-3.40.0.5"
    )
    internal_h2o_version_client.create_version(
        internal_h2o_version_id="3.40.0.6",
        image="h2o-3.40.0.6",
        aliases=["latest"],
    )
