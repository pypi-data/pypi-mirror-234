import http
import time

import pytest

from h2o_engine_manager.clients.exception import ApiException
from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_delete_internal_dai_version(internal_dai_version_client, internal_dai_versions_cleanup_after):
    v = internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.6-delete",
        image="dai-1.10.6-delete"
    )

    internal_dai_version_client.delete_version(internal_dai_version_id=v.internal_dai_version_id)

    time.sleep(CACHE_SYNC_SECONDS)

    with pytest.raises(ApiException) as exc:
        internal_dai_version_client.get_version(internal_dai_version_id=v.internal_dai_version_id)
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
