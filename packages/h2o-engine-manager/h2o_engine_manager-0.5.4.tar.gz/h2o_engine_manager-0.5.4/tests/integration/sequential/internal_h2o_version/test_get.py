import http
import time

import pytest

from h2o_engine_manager.clients.exception import ApiException
from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_get(internal_h2o_version_client, internal_h2o_versions_cleanup_after):
    internal_h2o_version_client.create_version(
        internal_h2o_version_id="3.40.0.3-get",
        image="3.40.0.3-get",
        aliases=["some-alias"]
    )

    # Wait to make sure the created h2o version is synced in cache.
    time.sleep(CACHE_SYNC_SECONDS)

    v = internal_h2o_version_client.get_version(internal_h2o_version_id="3.40.0.3-get")

    assert v.name == "internalH2OVersions/3.40.0.3-get"
    assert v.version == "3.40.0.3-get"
    assert v.internal_h2o_version_id == "3.40.0.3-get"

    # Test getting by alias
    v_alias = internal_h2o_version_client.get_version(internal_h2o_version_id="some-alias")

    # Need to compare field by field (v and v_alias are different objects but with same values)
    assert v.name == v_alias.name
    assert v.internal_h2o_version_id == v_alias.internal_h2o_version_id
    assert v.version == v_alias.version
    assert v.image == v_alias.image
    assert v.image_pull_policy == v_alias.image_pull_policy
    assert v.image_pull_secrets == v_alias.image_pull_secrets
    assert v.aliases == v_alias.aliases
    assert v.gpu_resource_name == v_alias.gpu_resource_name
    assert v.deprecated == v_alias.deprecated
    assert v.annotations == v_alias.annotations


def test_get_not_found(internal_h2o_version_client):
    with pytest.raises(ApiException) as exc:
        internal_h2o_version_client.get_version(internal_h2o_version_id="non-existing")
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
