import http
import time

import pytest

from h2o_engine_manager.clients.exception import ApiException
from tests.integration.conftest import CACHE_SYNC_SECONDS
from tests.integration.sequential.dai_profile.create_profile_request import *


def test_delete_validation(dai_profile_client):
    with pytest.raises(ApiException) as exc:
        dai_profile_client.delete_profile(profile_id="notfound")
    assert exc.value.status == http.HTTPStatus.NOT_FOUND

    with pytest.raises(ApiException) as exc:
        dai_profile_client.delete_profile(profile_id="invalid id")
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


def test_delete(dai_profile_client, dai_profile_cleanup_after):
    # When
    req = CreateDAIProfileRequest(profile_id="delete1")
    create_profile_from_request(dai_profile_client, req)
    time.sleep(CACHE_SYNC_SECONDS)

    # Then
    dai_profile_client.delete_profile(profile_id="delete1")

    time.sleep(CACHE_SYNC_SECONDS)

    with pytest.raises(ApiException) as exc:
        dai_profile_client.delete_profile(profile_id="delete1")
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
