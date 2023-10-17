import http
import time

import pytest

from h2o_engine_manager.clients.exception import ApiException
from tests.integration.conftest import CACHE_SYNC_SECONDS
from tests.integration.sequential.dai_profile.create_profile_request import *


def test_get_validation(dai_profile_client):
    with pytest.raises(ApiException) as exc:
        dai_profile_client.get_profile(profile_id="notfound")
    assert exc.value.status == http.HTTPStatus.NOT_FOUND

    with pytest.raises(ApiException) as exc:
        dai_profile_client.get_profile(profile_id="invalid id")
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


def test_get(dai_profile_client, dai_profile_cleanup_after):
    # When
    req = CreateDAIProfileRequest(profile_id="get1")
    create_profile_from_request(dai_profile_client, req)
    time.sleep(CACHE_SYNC_SECONDS)

    # Then
    profile = dai_profile_client.get_profile(profile_id="get1")

    assert profile.name == "daiProfiles/get1"
    assert profile.dai_profile_id == "get1"
    assert profile.cpu == 1
    assert profile.gpu == 0
    assert profile.display_name == ""
    assert profile.memory_bytes == "1Gi"
    assert profile.storage_bytes == "1Gi"
