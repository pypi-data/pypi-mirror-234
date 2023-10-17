import http
import os
import time

import pytest
from kubernetes import client
from kubernetes import config

from h2o_engine_manager.clients.dai_engine.dai_engine import DAIEngine
from h2o_engine_manager.clients.dai_engine.dai_engine_client import DAIEngineClient
from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from h2o_engine_manager.clients.exception import ApiException
from tests.integration.conftest import CACHE_SYNC_SECONDS


@pytest.mark.timeout(900)
def test_update(dai_client):
    workspace_id = "e1"
    engine_id = "e2e-tests"
    engine = create_dai_engine(
        dai_client=dai_client, workspace_id=workspace_id, engine_id=engine_id
    )

    try:
        engine.pause()
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_PAUSED.name

        # No DAI engine spec has been changed but the update_time should be
        # non-empty.
        engine.update()
        first_update_time = engine.update_time
        assert first_update_time is not None

        # The precision of update_time is only seconds. Need to wait at least one
        # second to check that next Update operation will update update_time.
        time.sleep(1)

        # Update one field (gpu) using wildcard.
        engine.gpu = 5
        engine.update()

        assert engine.gpu == 5
        second_update_time = engine.update_time
        assert second_update_time > first_update_time

        # Update multiple fields (gpu, annotations and display name).
        # Ignore update of fields that are not in update mask (cpu).
        engine.gpu = 0
        engine.cpu = 50
        engine.annotations = {
            "customKey1": "custom value 1",
            "customKey2": "custom value 2",
        }
        engine.display_name = "New display name"

        engine.update(update_mask="gpu,annotations,display_name")

        assert engine.gpu == 0
        assert engine.cpu != 50
        assert engine.annotations == {
            "customKey1": "custom value 1",
            "customKey2": "custom value 2",
        }
        assert engine.display_name == "New display name"

        # Remove display_name and check that custom annotations remained unchanged.
        # (sort of white-box testing - display_name is stored together with
        # annotations in kubeObject Annotations - want to make sure the update
        # does not interfere)
        engine.display_name = ""
        engine.update()

        assert engine.display_name == ""
        assert engine.annotations == {
            "customKey1": "custom value 1",
            "customKey2": "custom value 2",
        }

        # Update durations.
        engine.max_idle_duration = "361s"
        engine.max_running_duration = "360s"
        engine.update()

        assert engine.max_idle_duration == "361s"
        assert engine.max_running_duration == "6m"
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


@pytest.mark.timeout(900)
def test_update_validate_only(dai_client):
    workspace_id = "e1"
    engine_id = "update-validate"
    engine = create_dai_engine(
        dai_client=dai_client, workspace_id=workspace_id, engine_id=engine_id
    )

    try:
        engine.pause()
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_PAUSED.name

        original_cpu = engine.cpu
        assert original_cpu != 4
        engine.cpu = 4

        engine.update(update_mask="cpu", validate_only=True)

        # Response should contain the updated field
        # (as if the update was truly performed).
        assert engine.cpu == 4

        # Double check that engine is still unchanged.
        time.sleep(CACHE_SYNC_SECONDS)
        engine = dai_client.get_engine(
            engine_id=engine.engine_id, workspace_id=engine.workspace_id
        )

        assert engine.cpu == original_cpu
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


@pytest.mark.timeout(900)
def test_update_config(dai_client):
    workspace_id = "e1"
    engine_id = "update-config"
    config.load_config()
    engine = create_dai_engine(
        dai_client=dai_client, workspace_id=workspace_id, engine_id=engine_id
    )
    try:
        engine.pause()
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_PAUSED.name

        assert engine.config == {"key1": "val1", "key2": "val2"}

        engine.config = {
            "key1": "newVal1",
            "key3": "val3",
        }
        engine.update(update_mask="config")

        assert engine.config == {"key1": "newVal1", "key3": "val3"}

        # Extra white-box testing using k8s client to check that baseConfig in CRD object is not
        # affected by this update action (we cannot verify directly via AIEM API as its hidden).
        api_instance = client.CustomObjectsApi()
        kube_eng = api_instance.get_namespaced_custom_object(
            group="engine.h2o.ai",
            version="v1alpha1",
            namespace=os.getenv("TEST_K8S_WORKLOADS_NAMESPACE"),
            plural="driverlessais",
            name=f"{engine.workspace_id}.{engine.engine_id}",
        )

        # Check some base config fields.
        kube_config = kube_eng["spec"]["configuration"]
        assert kube_config["authentication_method"] == "oidc"
        assert (
            kube_config["base_url"]
            == f"/workspaces/{engine.workspace_id}/daiEngines/{engine.engine_id}/"
        )
        assert kube_config["enable_startup_checks"] == "false"
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


@pytest.mark.timeout(900)
def test_update_precondition(dai_client):
    workspace_id = "e1"
    engine_id = "test-update"
    engine = create_dai_engine(
        dai_client=dai_client, workspace_id=workspace_id, engine_id=engine_id
    )
    try:
        engine.pause()
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_PAUSED.name

        engine.resume()
        with pytest.raises(ApiException) as exc:
            engine.update()
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


def create_dai_engine(
    dai_client: DAIEngineClient, workspace_id: str, engine_id: str
) -> DAIEngine:
    want_version = "mock"

    engine = dai_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        version=want_version,
        cpu=1,
        gpu=0,
        memory_bytes="1Gi",
        storage_bytes="1Gi",
        max_idle_duration="15m",
        max_running_duration="2d",
        display_name="My engine 1",
        config={"key1": "val1", "key2": "val2"},
    )
    engine.wait()

    return engine
