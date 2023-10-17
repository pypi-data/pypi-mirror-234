import os
import time

from h2o_engine_manager.clients.h2o_engine.state import H2OEngineState
from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_get(h2o_engine_client):
    workspace_id = "get-h2o-engine"
    engine_id = "engine1"

    # Given
    h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        version="latest",
        node_count=1,
        cpu=1,
        gpu=0,
        memory_bytes="2Gi",
        max_idle_duration="2h",
        max_running_duration="12h",
        display_name="Proboscis monkey",
        annotations={"foo": "bar"},
    )

    time.sleep(CACHE_SYNC_SECONDS)

    # When
    e = h2o_engine_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)

    # Then
    assert e.name == f"workspaces/{workspace_id}/h2oEngines/{engine_id}"
    assert e.state == H2OEngineState.STATE_STARTING
    assert e.reconciling is True
    assert e.version == "0.0.0.0-latest"
    assert e.node_count == 1
    assert e.cpu == 1
    assert e.gpu == 0
    assert e.max_idle_duration == "2h"
    assert e.max_running_duration == "12h"
    assert e.display_name == "Proboscis monkey"
    assert e.annotations == {"foo": "bar"}
    assert e.create_time is not None
    assert e.delete_time is None
    external_hostname = os.getenv("MANAGER_EXTERNAL_HOSTNAME")
    assert (
        e.api_url
        == f"https://{external_hostname}/workspaces/{workspace_id}/h2oEngines/{engine_id}"
    )
    assert (
        e.login_url
        == f"https://{external_hostname}/workspaces/{workspace_id}/h2oEngines/{engine_id}/flow/index.html"
    )
    assert e.creator == "users/a3c6ab45-3bbb-4033-9e38-7f769d186b1a"
    assert e.creator_display_name == "aiem-test-user"
    assert e.memory_bytes == "2Gi"
