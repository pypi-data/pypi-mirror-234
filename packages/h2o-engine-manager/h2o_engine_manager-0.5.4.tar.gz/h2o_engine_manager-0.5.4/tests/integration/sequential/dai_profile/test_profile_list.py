import http
import time

import pytest

from h2o_engine_manager.clients.exception import ApiException
from tests.integration.conftest import CACHE_SYNC_SECONDS
from tests.integration.sequential.dai_profile.create_profile_request import *


def create_profiles(dai_profile_client):
    req1 = CreateDAIProfileRequest(
        profile_id="profile1", cpu=1, gpu=3, memory_bytes="3Gi", storage_bytes="3Gi", display_name="my best profile"
    )
    req2 = CreateDAIProfileRequest(
        profile_id="profile2", cpu=2, gpu=2, memory_bytes="8Gi", storage_bytes="128Gi", display_name="my second best profile"
    )
    req3 = CreateDAIProfileRequest(
        profile_id="profile3", cpu=2, gpu=1, memory_bytes="16Gi", storage_bytes="32Gi", display_name="my third best profile"
    )
    create_profile_from_request(dai_profile_client, req1)
    create_profile_from_request(dai_profile_client, req2)
    create_profile_from_request(dai_profile_client, req3)

    time.sleep(CACHE_SYNC_SECONDS)


@pytest.mark.parametrize(
    ["page_size", "page_token"],
    [
        (-20, ""),
        (0, "non-existing-token"),
    ],
)
def test_list_validation(
        dai_profile_client, page_size, page_token
):
    with pytest.raises(ApiException) as exc:
        dai_profile_client.list_profiles(
            page_size=page_size,
            page_token=page_token,
        )
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


def test_list(dai_profile_client, dai_profile_cleanup_after):
    # Test no profiles found.
    page = dai_profile_client.list_profiles()
    assert len(page.profiles) == 0
    assert page.next_page_token == ""
    assert page.total_size == 0

    # Arrange
    create_profiles(dai_profile_client=dai_profile_client)

    # Test getting first page.
    page = dai_profile_client.list_profiles(page_size=1)
    assert len(page.profiles) == 1
    assert page.next_page_token != ""
    assert page.total_size == 3

    # Test getting second page.
    page = dai_profile_client.list_profiles(
        page_size=1, page_token=page.next_page_token
    )
    assert len(page.profiles) == 1
    assert page.next_page_token != ""
    assert page.total_size == 3

    # Test getting last page.
    page = dai_profile_client.list_profiles(
        page_size=1, page_token=page.next_page_token
    )
    assert len(page.profiles) == 1
    assert page.next_page_token == ""
    assert page.total_size == 3

    # Test exceeding max page size.
    page = dai_profile_client.list_profiles(page_size=1001)
    assert len(page.profiles) == 3
    assert page.next_page_token == ""
    assert page.total_size == 3


def test_list_all(dai_profile_client, dai_profile_cleanup_after):
    create_profiles(dai_profile_client=dai_profile_client)

    # Test basic list_all.
    profiles = dai_profile_client.list_all_profiles()
    assert len(profiles) == 3