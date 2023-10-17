import http
import time

import pytest

from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from h2o_engine_manager.clients.exception import ApiException
from tests.integration.api.dai.create_dai_request import CreateDAIEngineRequest
from tests.integration.api.dai.create_dai_request import create_dai_from_request
from tests.integration.conftest import CACHE_SYNC_SECONDS


# Migrate creator test must be performed in tests
# that run also operator because the engine needs to be connected to.
@pytest.mark.timeout(600)
def test_migrate_creator(dai_client, dai_admin_client):
    workspace_id = "set-creator"
    engine_id = "e1"
    aiem_test_admin_user = (
        "fd138058-c564-4bed-a7b9-e63a5eb6348d"  # taken from the platform token
    )
    req = CreateDAIEngineRequest(
        workspace_id=workspace_id,
        engine_id=engine_id,
        memory_bytes="8Gi",
        storage_bytes="8Gi",
        version="1.10.5"
    )
    # Create an engine as the aiem-test-user user
    eng = create_dai_from_request(dai_client, req)
    time.sleep(CACHE_SYNC_SECONDS)
    try:
        # Get the engine as an admin user
        eng_admin = dai_admin_client.get_engine(
            engine_id=engine_id, workspace_id=workspace_id
        )

        # Only stopped engine can be migrated.
        assert eng.state != DAIEngineState.STATE_PAUSED
        with pytest.raises(ApiException) as exc:
            eng_admin.migrate_creator(new_creator=aiem_test_admin_user)
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST

        # Pause the engine
        eng.pause()
        eng.wait()

        # Only admin can set creator.
        with pytest.raises(ApiException) as exc:
            eng.migrate_creator(new_creator=aiem_test_admin_user)
        assert exc.value.status == http.HTTPStatus.FORBIDDEN

        # Migrate creator as an admin user, connect to it as a new creator
        eng_admin.migrate_creator(new_creator=aiem_test_admin_user)
        eng_admin.resume()
        eng_admin.wait()
        eng_admin.connect()

    finally:
        dai_admin_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )
