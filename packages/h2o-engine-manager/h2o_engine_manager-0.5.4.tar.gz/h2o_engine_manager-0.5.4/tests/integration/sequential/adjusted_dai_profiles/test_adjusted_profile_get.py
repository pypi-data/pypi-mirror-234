import http
import time

import pytest

from h2o_engine_manager.clients.adjusted_dai_profile.adjusted_profile import (
    AdjustedDAIProfile,
)
from h2o_engine_manager.clients.exception import ApiException
from tests.integration.conftest import CACHE_SYNC_SECONDS
from tests.integration.sequential.dai_profile.create_profile_request import *


def create_test_profile(dai_profile_client) -> DAIProfile:
    req = CreateDAIProfileRequest(
        profile_id="my-profile",
        cpu=30,
        gpu=999,
        memory_bytes="1000Gi",
        storage_bytes="1000Gi",
    )
    profile = create_profile_from_request(dai_profile_client, req)

    time.sleep(CACHE_SYNC_SECONDS)

    return profile


def test_get_validation(adjusted_dai_profile_client, dai_profile_cleanup_after):
    with pytest.raises(ApiException) as exc:
        adjusted_dai_profile_client.get_adjusted_profile(profile_id="notfound", workspace_id="notfound")
    assert exc.value.status == http.HTTPStatus.NOT_FOUND

    with pytest.raises(ApiException) as exc:
        adjusted_dai_profile_client.get_adjusted_profile(profile_id="invalid profile id", workspace_id="notfound")
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST

    with pytest.raises(ApiException) as exc:
        adjusted_dai_profile_client.get_adjusted_profile(profile_id="notfound", workspace_id="invalid workspace id")
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


def test_get(dai_profile_client, adjusted_dai_profile_client, dai_profile_cleanup_after):
    # DAISetup objects are created separately via setup script.
    # TODO create DAISetup objects here manually once the DAISetup API is finished.

    # When
    create_test_profile(dai_profile_client)

    # Then
    p = adjusted_dai_profile_client.get_adjusted_profile(profile_id="my-profile", workspace_id="adjusted-dai-profiles")
    expected = AdjustedDAIProfile(
        cpu=20,
        adjusted_cpu_reason="source DAI Profile value: 30, maximum allowed by the workspace constraints: 20",
        gpu=30,
        adjusted_gpu_reason="source DAI Profile value: 999, maximum allowed by the workspace constraints: 30",
        memory_bytes="1000Gi",
        adjusted_memory_bytes_reason="",
        storage_bytes="1000Gi",
        adjusted_storage_bytes_reason="",
        name="daiProfiles/my-profile",
        display_name="",
    )
    assert p.__dict__ == expected.__dict__

