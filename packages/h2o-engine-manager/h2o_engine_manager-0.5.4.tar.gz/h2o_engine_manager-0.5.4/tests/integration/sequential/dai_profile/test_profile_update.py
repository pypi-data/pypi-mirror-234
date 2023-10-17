import http
import time

import pytest

from h2o_engine_manager.clients.exception import ApiException
from tests.integration.conftest import CACHE_SYNC_SECONDS


@pytest.mark.parametrize(
    "mask",
    [
        "unknown",
        "invalid character",
        "gpu, *",
        " ",
    ],
)
def test_update_mask_validation(dai_profile_client, mask, dai_profile_cleanup_after):
    profile = dai_profile_client.create_profile(
        profile_id="profile1",
        cpu=1,
        gpu=0,
        memory_bytes="1Gi",
        storage_bytes="1Gi",
        display_name="Smokerinho",
    )
    profile.display_name = "Changed Smokerinho"

    with pytest.raises(ApiException) as exc:
        dai_profile_client.update_profile(profile=profile, update_mask=mask)
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


def test_update(dai_profile_client, dai_profile_cleanup_after):
    # Create profile.
    original = dai_profile_client.create_profile(
        profile_id="profile1",
        cpu=1,
        gpu=0,
        memory_bytes="1Gi",
        storage_bytes="1Gi",
        display_name="Smokerinho",
    )

    time.sleep(CACHE_SYNC_SECONDS)

    original.cpu = 2
    original.gpu = 1
    original.memory_bytes = "2Mi"
    original.storage_bytes = "200Gi"

    # Update profile with update_mask.
    updated = dai_profile_client.update_profile(original, update_mask="cpu,memory_bytes")

    assert updated.cpu == 2
    assert updated.memory_bytes == "2Mi"
    assert updated.gpu == 0

    # Update profile without update_mask.
    updated = dai_profile_client.update_profile(original)

    assert updated.gpu == 1
