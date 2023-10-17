import http

import pytest

from h2o_engine_manager.clients.exception import ApiException
from tests.integration.sequential.dai_profile.create_profile_request import *


def incorrect_profile_id(req: CreateDAIProfileRequest) -> CreateDAIProfileRequest:
    req.profile_id = ""
    return req


def cpu_below_min(req: CreateDAIProfileRequest) -> CreateDAIProfileRequest:
    req.cpu = 0
    return req


def gpu_below_min(req: CreateDAIProfileRequest) -> CreateDAIProfileRequest:
    req.gpu = -5
    return req


def memory_below_min(req: CreateDAIProfileRequest) -> CreateDAIProfileRequest:
    req.memory_bytes = "0"
    return req


def incorrect_storage(req: CreateDAIProfileRequest) -> CreateDAIProfileRequest:
    req.storage_bytes = "-2"
    return req


def incorrect_display_name(req: CreateDAIProfileRequest) -> CreateDAIProfileRequest:
    req.display_name = "I am definitely longer than 63 characters, there's no way I can pass validation"
    return req


def test_create_profile(dai_profile_client, dai_profile_cleanup_after):
    # When
    profile = dai_profile_client.create_profile(
        profile_id="profile1",
        cpu=1,
        gpu=0,
        memory_bytes="1Gi",
        storage_bytes="1Gi",
        display_name="Proboscis monkey",
    )

    # Then
    assert profile.name == "daiProfiles/profile1"
    assert profile.dai_profile_id == "profile1"
    assert profile.cpu == 1
    assert profile.gpu == 0
    assert profile.display_name == "Proboscis monkey"
    assert profile.memory_bytes == "1Gi"
    assert profile.storage_bytes == "1Gi"


@pytest.mark.parametrize(
    "modify_func",
    [
        incorrect_profile_id,
        cpu_below_min,
        gpu_below_min,
        memory_below_min,
        incorrect_display_name,
    ],
)
def test_create_profile_server_validation(dai_profile_client, modify_func, dai_profile_cleanup_after):
    # When
    req = modify_func(CreateDAIProfileRequest(profile_id="create-validation"))

    # Then
    with pytest.raises(ApiException) as exc:
        create_profile_from_request(dai_profile_client, req)
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize(
    "modify_func", [incorrect_storage]
)
def test_create_profile_client_validation(dai_profile_client, modify_func, dai_profile_cleanup_after):
    # When
    req = modify_func(CreateDAIProfileRequest(profile_id="create-validation"))

    # Then
    with pytest.raises(ValueError):
        create_profile_from_request(dai_profile_client, req)


def test_create_already_exists(dai_profile_client, dai_profile_cleanup_after):
    # When a profile is created
    req = CreateDAIProfileRequest(profile_id="create-already-exists")
    create_profile_from_request(dai_profile_client, req)

    # Then profile with the same IDs cannot be created again.
    with pytest.raises(ApiException) as exc:
        create_profile_from_request(dai_profile_client, req)
    assert exc.value.status == http.HTTPStatus.CONFLICT
