import http

import pytest

from h2o_engine_manager.clients.adjusted_dai_profile.client import (
    AdjustedDAIProfileClient,
)
from h2o_engine_manager.clients.exception import ApiException
from tests.integration.sequential.dai_profile.test_profile_list import create_profiles

workspace_id = "adjusted-dai-profiles"


@pytest.mark.parametrize(
    ["page_size", "page_token"],
    [
        (-20, ""),
        (0, "non-existing-token"),
    ],
)
def test_list_validation(
    adjusted_dai_profile_client,
    page_size,
    page_token,
    dai_profile_cleanup_after,
):
    with pytest.raises(ApiException) as exc:
        adjusted_dai_profile_client.list_adjusted_profiles(
            workspace_id=workspace_id,
            page_size=page_size,
            page_token=page_token,
        )
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


def test_list(
    dai_profile_client,
    adjusted_dai_profile_client: AdjustedDAIProfileClient,
    dai_profile_cleanup_after,
):
    # Test no profiles found.
    page = adjusted_dai_profile_client.list_adjusted_profiles(workspace_id=workspace_id)
    assert len(page.adjusted_profiles) == 0
    assert page.next_page_token == ""
    assert page.total_size == 0

    # Arrange
    create_profiles(dai_profile_client=dai_profile_client)

    # Test getting first page.
    page = adjusted_dai_profile_client.list_adjusted_profiles(workspace_id=workspace_id, page_size=1)
    assert len(page.adjusted_profiles) == 1
    assert page.next_page_token != ""
    assert page.total_size == 3

    # Test getting second page.
    page = adjusted_dai_profile_client.list_adjusted_profiles(
        workspace_id=workspace_id, page_size=1, page_token=page.next_page_token
    )
    assert len(page.adjusted_profiles) == 1
    assert page.next_page_token != ""
    assert page.total_size == 3

    # Test getting last page.
    page = adjusted_dai_profile_client.list_adjusted_profiles(
        workspace_id=workspace_id, page_size=1, page_token=page.next_page_token
    )
    assert len(page.adjusted_profiles) == 1
    assert page.next_page_token == ""
    assert page.total_size == 3

    # Test exceeding max page size.
    page = adjusted_dai_profile_client.list_adjusted_profiles(workspace_id=workspace_id, page_size=1001)
    assert len(page.adjusted_profiles) == 3
    assert page.next_page_token == ""
    assert page.total_size == 3


def test_list_all(dai_profile_client, adjusted_dai_profile_client, dai_profile_cleanup_after):
    create_profiles(dai_profile_client)

    # Test basic list_all.
    profiles = adjusted_dai_profile_client.list_all_adjusted_profiles(workspace_id=workspace_id)
    assert len(profiles) == 3
