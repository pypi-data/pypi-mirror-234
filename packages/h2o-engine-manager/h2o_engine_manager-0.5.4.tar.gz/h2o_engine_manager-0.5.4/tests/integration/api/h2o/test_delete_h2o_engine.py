import http
import time

import pytest

from h2o_engine_manager.clients.exception import ApiException
from h2o_engine_manager.clients.h2o_engine.state import H2OEngineState
from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_delete_validate_only(h2o_engine_client):
    workspace_id = "delete-h2o-validate"
    engine_id = "e1"

    e = h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        version="3.40.0.3",
        node_count=1,
        cpu=1,
        gpu=0,
        max_idle_duration="5h",
        max_running_duration="10h",
    )

    e.delete(validate_only=True)

    # Although not deleted, the response should behave as if it was deleted.
    # Double-check that engine still exists (no exception is thrown) and it's not in DELETING state.
    time.sleep(CACHE_SYNC_SECONDS)
    e = h2o_engine_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)
    assert e.state != H2OEngineState.STATE_DELETING


def test_delete(h2o_engine_client):
    workspace_id = "delete-h2o"
    engine_id = "e1"

    e = h2o_engine_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        version="3.40.0.3",
        node_count=1,
        cpu=1,
        gpu=0,
        max_idle_duration="5h",
        max_running_duration="10h",
    )

    e.delete()

    # This test case is supposed to run in simplified test environment. Therefore, it can happen
    # that the engine was deleted so quickly, that AIEM had nothing to return.
    # Check delete-related fields only if the engine was returned by AIEM.
    if e is not None:
        assert e.delete_time is not None
        assert e.state == H2OEngineState.STATE_DELETING

    # Check that the engine is not found after some time (is deleted).
    e.wait(timeout_seconds=10)

    with pytest.raises(ApiException) as exc:
        h2o_engine_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)
    assert exc.value.status == http.HTTPStatus.NOT_FOUND
