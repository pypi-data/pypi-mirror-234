import http
import time

import pytest

from h2o_engine_manager.clients.exception import ApiException
from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_delete(internal_h2o_version_client, internal_h2o_versions_cleanup_after):
    v = internal_h2o_version_client.create_version(
        internal_h2o_version_id="3.40.0.3-delete",
        image="h2o-3.40.0.3-delete"
    )

    internal_h2o_version_client.delete_version(internal_h2o_version_id=v.internal_h2o_version_id)

    time.sleep(CACHE_SYNC_SECONDS)

    with pytest.raises(ApiException) as exc:
        internal_h2o_version_client.get_version(internal_h2o_version_id=v.internal_h2o_version_id)
    assert exc.value.status == http.HTTPStatus.NOT_FOUND


def test_delete_by_alias(internal_h2o_version_client, internal_h2o_versions_cleanup_after):
    v = internal_h2o_version_client.create_version(
        internal_h2o_version_id="3.40.0.3-delete-by-alias",
        image="h2o-3.40.0.3-delete-by-alias",
        aliases=["aaaaaa"],
    )

    internal_h2o_version_client.delete_version(internal_h2o_version_id="aaaaaa")

    time.sleep(CACHE_SYNC_SECONDS)

    with pytest.raises(ApiException) as exc:
        internal_h2o_version_client.get_version(internal_h2o_version_id=v.internal_h2o_version_id)
    assert exc.value.status == http.HTTPStatus.NOT_FOUND

    with pytest.raises(ApiException) as exc:
        internal_h2o_version_client.get_version(internal_h2o_version_id="aaaaaa")
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
