import os
import subprocess
import time

from h2o_engine_manager.clients.engine.state import EngineState
from h2o_engine_manager.clients.engine.type import EngineType
from tests.integration.api.dai.create_dai_request import CreateDAIEngineRequest
from tests.integration.api.dai.create_dai_request import create_dai_from_request
from tests.integration.conftest import CACHE_SYNC_SECONDS


def create_engines(dai_client, h2o_engine_client, workspace_id):
    req1 = CreateDAIEngineRequest(
        workspace_id=workspace_id,
        engine_id="engine1",
        display_name="My engine 1",
        cpu=1,
        version="1.10.4",
        memory_bytes="1Mi",
        storage_bytes="1Ki",
        annotations={"e1": "v1"},
    )
    req2 = CreateDAIEngineRequest(
        workspace_id=workspace_id,
        engine_id="engine2",
        display_name="My engine 2",
        cpu=4,
        version="1.10.5",
        memory_bytes="1Ki",
        storage_bytes="1Ki",
        annotations={"e2": "v2"},
    )
    req3 = CreateDAIEngineRequest(
        workspace_id=workspace_id,
        engine_id="engine3",
        display_name="My engine 3",
        cpu=1,
        version="1.10.4",
        memory_bytes="1Ki",
        storage_bytes="1Ki",
        annotations={"e3": "v3"},
    )
    requests = [req1, req2, req3]

    for req in requests:
        create_dai_from_request(dai_client, req)

    # We cannot create engine with deprecated version.
    # Workaround: manually set daiEngine1's and daiEngine3's version 1.10.4 to a deprecated version 1.10.3.
    # (overwriting annotation in the CRD object)
    subprocess.run(
        [
            "kubectl",
            "annotate",
            "--overwrite",
            f"--namespace={os.getenv('TEST_K8S_WORKLOADS_NAMESPACE')}",
            "dai",
            f"{workspace_id}.engine1",
            "engine.h2o.ai/version=1.10.3"
        ]
    )
    subprocess.run(
        [
            "kubectl",
            "annotate",
            "--overwrite",
            f"--namespace={os.getenv('TEST_K8S_WORKLOADS_NAMESPACE')}",
            "dai",
            f"{workspace_id}.engine3",
            "engine.h2o.ai/version=1.10.3"
        ]
    )


    h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id="engine1",
        version="3.36.1.5",
        node_count=1,
        cpu=2,
        gpu=0,
        memory_bytes="1Mi",
        max_idle_duration="2h",
        max_running_duration="12h",
    )
    h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id="engine2",
        version="3.38.0.4",
        node_count=1,
        cpu=2,
        gpu=0,
        memory_bytes="1Ki",
        max_idle_duration="2h",
        max_running_duration="12h",
    )
    h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id="engine3",
        version="3.40.0.3",
        node_count=1,
        cpu=3,
        gpu=1,
        memory_bytes="1Mi",
        max_idle_duration="2h",
        max_running_duration="12h",
    )

    time.sleep(CACHE_SYNC_SECONDS)


def test_list(engine_client, dai_client, h2o_engine_client):
    workspace_id = "list-generic-engines"
    create_engines(dai_client, h2o_engine_client, workspace_id)

    # When list first page
    page = engine_client.list_engines(workspace_id=workspace_id, page_size=2)

    # Then
    assert len(page.engines) == 2
    assert page.total_size == 6
    assert page.next_page_token != ""

    # When list second page
    page = engine_client.list_engines(
        workspace_id=workspace_id, page_size=2, page_token=page.next_page_token
    )

    # Then
    assert len(page.engines) == 2
    assert page.total_size == 6
    assert page.next_page_token != ""

    # When list third page
    page = engine_client.list_engines(
        workspace_id=workspace_id, page_size=1, page_token=page.next_page_token
    )

    # Then
    assert len(page.engines) == 1
    assert page.total_size == 6
    assert page.next_page_token != ""

    # When list fourth (last) page
    page = engine_client.list_engines(
        workspace_id=workspace_id, page_size=1, page_token=page.next_page_token
    )

    # Then
    assert len(page.engines) == 1
    assert page.total_size == 6
    assert page.next_page_token == ""

    # When order_by
    page = engine_client.list_engines(
        workspace_id=workspace_id,
        order_by="cpu desc, version desc, memory_bytes desc, storage_bytes asc",
    )

    # Then
    assert len(page.engines) == 6
    assert page.total_size == 6
    assert page.next_page_token == ""
    assert (
        page.engines[0].name == f"workspaces/{workspace_id}/daiEngines/engine2"
    )  # highest cpu (4)
    assert (
        page.engines[1].name == f"workspaces/{workspace_id}/h2oEngines/engine3"
    )  # second-highest cpu (3)
    assert (
        page.engines[2].name == f"workspaces/{workspace_id}/h2oEngines/engine2"
    )  # highest version (3.40.0.3)
    assert (
        page.engines[3].name == f"workspaces/{workspace_id}/h2oEngines/engine1"
    )  # second-highest version (3.38.0.4)
    assert (
        page.engines[4].name == f"workspaces/{workspace_id}/daiEngines/engine1"
    )  # highest memory_bytes (1Mi)
    assert page.engines[5].name == f"workspaces/{workspace_id}/daiEngines/engine3"

    # When filter non-existing
    page = engine_client.list_engines(
        workspace_id=workspace_id,
        filter_expr="type != TYPE_DRIVERLESS_AI AND type != TYPE_H2O",
    )

    # Then
    assert len(page.engines) == 0
    assert page.total_size == 0
    assert page.next_page_token == ""

    # When filter engines with deprecated version
    page = engine_client.list_engines(
        workspace_id=workspace_id,
        filter_expr="deprecated_version = true",
    )

    # Then
    assert len(page.engines) == 2
    assert page.total_size == 2
    assert page.next_page_token == ""

    # Newly created engine is listed first.
    assert page.engines[0].name == f"workspaces/{workspace_id}/daiEngines/engine3"
    assert page.engines[0].version == "1.10.3"
    assert page.engines[0].deprecated_version is True

    assert page.engines[1].name == f"workspaces/{workspace_id}/daiEngines/engine1"
    assert page.engines[1].version == "1.10.3"
    assert page.engines[1].deprecated_version is True

    # When filter
    expr = "type = TYPE_DRIVERLESS_AI AND version < \"1.10.5\" AND memory_bytes > 1024"
    page = engine_client.list_engines(workspace_id=workspace_id, filter_expr=expr)

    # Then
    assert len(page.engines) == 1
    assert page.total_size == 1
    assert page.next_page_token == ""
    assert page.engines[0].name == f"workspaces/{workspace_id}/daiEngines/engine1"

    # Extra check for correct mapping (Since we don't have GetEngine endpoint)
    eng = page.engines[0]
    assert eng.version == "1.10.3"
    assert eng.deprecated_version is True
    assert eng.engine_type == EngineType.TYPE_DRIVERLESS_AI
    assert eng.cpu == 1
    assert eng.gpu == 0
    assert eng.create_time is not None
    assert eng.update_time is None
    assert eng.delete_time is None
    assert eng.annotations["e1"] == "v1"
    assert eng.display_name == "My engine 1"
    assert eng.memory_bytes == "1Mi"
    assert eng.storage_bytes == "1Ki"
    assert eng.reconciling is True
    assert eng.creator == "users/a3c6ab45-3bbb-4033-9e38-7f769d186b1a"
    assert eng.creator_display_name == "aiem-test-user"
    assert eng.state == EngineState.STATE_STARTING
    external_hostname = os.getenv("MANAGER_EXTERNAL_HOSTNAME")
    assert (
        eng.login_url
        == f"https://{external_hostname}/workspaces/list-generic-engines/daiEngines/engine1/oidc/login"
    )

    # List all
    engines = engine_client.list_all_engines(workspace_id=workspace_id)
    assert len(engines) == 6
