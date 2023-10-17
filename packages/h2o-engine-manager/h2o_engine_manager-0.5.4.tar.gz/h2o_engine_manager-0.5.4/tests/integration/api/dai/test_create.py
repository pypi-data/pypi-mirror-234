import http
import os
import time

import pytest

from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from h2o_engine_manager.clients.exception import ApiException
from tests.integration.api.dai.create_dai_request import *
from tests.integration.conftest import CACHE_SYNC_SECONDS
from tests.integration.sequential.adjusted_dai_profiles.test_adjusted_profile_get import (
    create_test_profile,
)


def incorrect_workspace_id(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.workspace_id = "no space in id allowed"
    return req


def incorrect_engine_id(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.engine_id = ""
    return req


def cpu_below_min(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.cpu = 0
    return req


def gpu_below_min(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.gpu = -5
    return req


def memory_below_min(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.memory_bytes = "1000"
    return req


def incorrect_storage(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.storage_bytes = "-2"
    return req


def incorrect_max_idle_duration(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.max_idle_duration = "-5s"
    return req


def incorrect_display_name(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.display_name = "I am definitely longer than 63 characters, there's no way I can pass validation"
    return req


def incorrect_version(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.version = "non-existing-version"
    return req


def deprecated_version(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.version = "1.10.3"
    return req


def incorrect_config(req: CreateDAIEngineRequest) -> CreateDAIEngineRequest:
    req.config = {"base_url": "whatever"}
    return req


def test_create_dai(dai_client):
    # When
    engine = dai_client.create_engine(
        workspace_id="create-dai",
        engine_id="engine1",
        version="1.10.5-mock",
        cpu=1,
        gpu=0,
        memory_bytes="1Gi",
        storage_bytes="1Gi",
        max_idle_duration="2h",
        max_running_duration="12h",
        display_name="Proboscis monkey",
        config={"key1": "val1"},
    )

    # Then
    assert engine.name == "workspaces/create-dai/daiEngines/engine1"
    assert engine.state == DAIEngineState.STATE_STARTING
    assert engine.reconciling is True
    assert engine.version == "1.10.5-mock"
    assert engine.cpu == 1
    assert engine.gpu == 0
    assert engine.max_idle_duration == "2h"
    assert engine.max_running_duration == "12h"
    assert engine.display_name == "Proboscis monkey"
    assert engine.annotations == {}
    assert engine.config == {"key1": "val1"}
    assert engine.create_time is not None
    assert engine.delete_time is None
    assert engine.resume_time is not None
    external_hostname = os.getenv("MANAGER_EXTERNAL_HOSTNAME")
    assert (
        engine.api_url
        == f"https://{external_hostname}/workspaces/create-dai/daiEngines/engine1"
    )
    assert (
        engine.login_url
        == f"https://{external_hostname}/workspaces/create-dai/daiEngines/engine1/oidc/login"
    )
    assert engine.creator == "users/a3c6ab45-3bbb-4033-9e38-7f769d186b1a"
    assert engine.creator_display_name == "aiem-test-user"
    assert engine.memory_bytes == "1Gi"
    assert engine.storage_bytes == "1Gi"


def test_create_dai_version_alias(dai_client):
    # When
    req = CreateDAIEngineRequest(
        workspace_id="create-dai-version-alias", version="alias-foo"
    )
    eng = create_dai_from_request(dai_client, req)

    # Then
    assert eng.version == "1.10.5-mock"


@pytest.mark.parametrize(
    "modify_func",
    [
        incorrect_workspace_id,
        incorrect_engine_id,
        cpu_below_min,
        gpu_below_min,
        memory_below_min,
        incorrect_display_name,
        incorrect_version,
        deprecated_version,
        incorrect_config,
    ],
)
def test_create_dai_server_validation(dai_client, modify_func):
    # When
    req = modify_func(CreateDAIEngineRequest(workspace_id="create-dai-validation"))

    # Then
    with pytest.raises(ApiException) as exc:
        create_dai_from_request(dai_client, req)
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize(
    "modify_func", [incorrect_storage, incorrect_max_idle_duration]
)
def test_create_dai_client_validation(dai_client, modify_func):
    # When
    req = modify_func(CreateDAIEngineRequest(workspace_id="create-dai-validation"))

    # Then
    with pytest.raises(ValueError) as exc:
        create_dai_from_request(dai_client, req)


def test_create_already_exists(dai_client):
    # When an engine is created
    req = CreateDAIEngineRequest(workspace_id="create-dai-already-exists")
    create_dai_from_request(dai_client, req)

    # Then engine with the same IDs cannot be created again.
    with pytest.raises(ApiException) as exc:
        create_dai_from_request(dai_client, req)
    assert exc.value.status == http.HTTPStatus.CONFLICT

    # Check that validate only also returns Conflict.
    req.validate_only = True
    with pytest.raises(ApiException) as exc:
        create_dai_from_request(dai_client, req)
    assert exc.value.status == http.HTTPStatus.CONFLICT


def test_create_validate_only(dai_client):
    # When engine is not really created
    req = CreateDAIEngineRequest(
        workspace_id="create-dai-validate-only", validate_only=True
    )
    create_dai_from_request(dai_client, req)

    # Then it cannot be found
    with pytest.raises(ApiException) as exc:
        dai_client.get_engine(
            workspace_id="create-dai-validate-only", engine_id="engine1"
        )
    assert exc.value.status == http.HTTPStatus.NOT_FOUND


def test_create_optional_values(dai_client):
    # Default values should be applied.
    e = dai_client.create_engine(
        workspace_id="dai-engine-optional-values", engine_id="e1"
    )
    assert e.cpu == 1
    assert e.gpu == 0
    assert e.memory_bytes == "1Gi"
    assert e.storage_bytes == "1Gi"
    assert e.max_idle_duration == "4h"
    assert e.max_running_duration == "4h"


def test_create_engine_id_generator(dai_client):
    # Engine ID should be uniquely generated if not provided
    no_param_1 = dai_client.create_engine(workspace_id="create-dai-generate-engine-id")
    time.sleep(CACHE_SYNC_SECONDS)
    no_param_2 = dai_client.create_engine(workspace_id="create-dai-generate-engine-id")
    assert no_param_1.name != no_param_2.name

    # Engine ID should be uniquely generated from display name
    display_name_1 = dai_client.create_engine(workspace_id="create-dai-generate-engine-id", display_name="Smoker@2023")
    time.sleep(CACHE_SYNC_SECONDS)
    display_name_2 = dai_client.create_engine(workspace_id="create-dai-generate-engine-id", display_name="Smoker@2023")
    assert display_name_1.name != display_name_2.name


def test_create_dai_with_profile(dai_profile_client, dai_client):
    # Setup
    profile = create_test_profile(dai_profile_client)

    try:
        # When
        req = CreateDAIEngineRequest(
            workspace_id="adjusted-dai-profiles",
            profile_id="my-profile",
            cpu=None,
            gpu=None,
            memory_bytes=None,
            storage_bytes=None,
            version="1.10.5-mock",
        )
        eng = create_dai_from_request(dai_client, req)

        # Then
        assert eng.cpu == 20
        assert eng.gpu == 30
        assert eng.memory_bytes == "1000Gi"
        assert eng.storage_bytes == "1000Gi"
    finally:
        dai_profile_client.delete_profile(profile_id=profile.dai_profile_id)
