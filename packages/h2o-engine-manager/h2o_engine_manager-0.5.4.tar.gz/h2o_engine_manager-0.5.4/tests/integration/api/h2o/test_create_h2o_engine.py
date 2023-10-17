import http
import json
import os
import time

import pytest

from h2o_engine_manager.clients.exception import ApiException
from h2o_engine_manager.clients.h2o_engine.state import H2OEngineState
from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_create(h2o_engine_client):
    # When
    engine = h2o_engine_client.create_engine(
        workspace_id="create-h2o-engine",
        engine_id="engine1",
        version="latest",
        node_count=2,
        cpu=1,
        gpu=0,
        memory_bytes="2Gi",
        max_idle_duration="2h",
        max_running_duration="12h",
        display_name="Proboscis monkey",
        annotations={"foo": "bar"},
    )

    # Then
    assert engine.name == "workspaces/create-h2o-engine/h2oEngines/engine1"
    assert engine.state == H2OEngineState.STATE_STARTING
    assert engine.reconciling is True
    assert engine.version == "0.0.0.0-latest"
    assert engine.node_count == 2
    assert engine.cpu == 1
    assert engine.gpu == 0
    assert engine.max_idle_duration == "2h"
    assert engine.max_running_duration == "12h"
    assert engine.display_name == "Proboscis monkey"
    assert engine.annotations == {"foo": "bar"}
    assert engine.create_time is not None
    assert engine.delete_time is None
    external_hostname = os.getenv("MANAGER_EXTERNAL_HOSTNAME")
    assert (
        engine.api_url
        == f"https://{external_hostname}/workspaces/create-h2o-engine/h2oEngines/engine1"
    )
    assert (
        engine.login_url
        == f"https://{external_hostname}/workspaces/create-h2o-engine/h2oEngines/engine1/flow/index.html"
    )
    assert engine.creator == "users/a3c6ab45-3bbb-4033-9e38-7f769d186b1a"
    assert engine.creator_display_name == "aiem-test-user"
    assert engine.memory_bytes == "2Gi"


def test_create_default_values(h2o_engine_client):
    # When
    engine = h2o_engine_client.create_engine(
        workspace_id="create-h2o-engine",
        engine_id="engine-default-values",
        version="latest",
    )

    # Then default values are filled from workspace constraints (see system.default H2OSetup)
    assert engine.node_count == 1
    assert engine.cpu == 1
    assert engine.gpu == 0
    assert engine.max_idle_duration == "1h"
    assert engine.max_running_duration == "4h"
    assert engine.memory_bytes == "4Gi"

    # Other fields are set according to API
    assert (
        engine.name == "workspaces/create-h2o-engine/h2oEngines/engine-default-values"
    )
    assert engine.state == H2OEngineState.STATE_STARTING
    assert engine.reconciling is True
    assert engine.version == "0.0.0.0-latest"
    assert engine.display_name == ""
    assert engine.annotations == {}
    assert engine.create_time is not None
    assert engine.delete_time is None
    external_hostname = os.getenv("MANAGER_EXTERNAL_HOSTNAME")
    assert (
        engine.api_url
        == f"https://{external_hostname}/workspaces/create-h2o-engine/h2oEngines/engine-default-values"
    )
    assert (
        engine.login_url
        == f"https://{external_hostname}/workspaces/create-h2o-engine/h2oEngines/engine-default-values/flow/index.html"
    )
    assert engine.creator == "users/a3c6ab45-3bbb-4033-9e38-7f769d186b1a"
    assert engine.creator_display_name == "aiem-test-user"


def test_create_validation(h2o_engine_client):
    with pytest.raises(ApiException) as exc:
        h2o_engine_client.create_engine(
            workspace_id="create-h2o-engine-validation",
            engine_id="engine1",
            version="latest",
            memory_bytes="1Mi",  # violates constraint for minimal memory bytes
        )
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


def test_create_validation_unavailable_version(h2o_engine_client):
    with pytest.raises(ApiException) as exc:
        h2o_engine_client.create_engine(
            workspace_id="create-h2o-engine-validation-unavailable-version",
            engine_id="engine1",
            version="foo",
        )
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST
    assert 'version "foo" is unavailable' == json.loads(exc.value.body)["message"]


def test_create_engine_id_generator(h2o_engine_client):
    # Engine ID should be uniquely generated if not provided
    no_param_1 = h2o_engine_client.create_engine(workspace_id="create-h2o-generate-engine-id", version="latest")
    time.sleep(CACHE_SYNC_SECONDS)
    no_param_2 = h2o_engine_client.create_engine(workspace_id="create-h2o-generate-engine-id", version="latest")
    assert no_param_1.name != no_param_2.name

    # Engine ID should be uniquely generated from display name
    display_name_1 = h2o_engine_client.create_engine(workspace_id="create-h2o-generate-engine-id", display_name="Smoker@2023", version="latest")
    time.sleep(CACHE_SYNC_SECONDS)
    display_name_2 = h2o_engine_client.create_engine(workspace_id="create-h2o-generate-engine-id", display_name="Smoker@2023", version="latest")
    assert display_name_1.name != display_name_2.name
