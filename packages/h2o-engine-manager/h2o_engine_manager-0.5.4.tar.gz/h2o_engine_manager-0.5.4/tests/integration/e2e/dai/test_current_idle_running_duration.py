import time

import pytest


# Overwriting default pytest timeout for this long-running test method.
@pytest.mark.timeout(600)
def test_current_idle_running_duration(dai_client):
    """
    Main goal of this is to verify the current idle and runtime duration is properly detected.
    """

    want_version = "mock"
    workspace_id = "default"
    engine_id = "e1"

    # Create engine
    engine = dai_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        version=want_version,
    )
    try:
        # Wait for RUNNING
        engine.wait()
        # Wait a few seconds
        time.sleep(10)
        e = dai_client.get_engine(workspace_id=workspace_id, engine_id=engine_id)
        # Verify the current idle and runtime duration.
        initial_idle = int(e.current_idle_duration.rstrip("s"))
        initial_runtime = int(e.current_running_duration.rstrip("s"))

        assert initial_idle > 5
        assert initial_runtime > 5

        e.pause()
        e.wait()
        e.resume()
        e.wait()

        # Verify the current idle and runtime resets with the engine resume (is lower than on the initial run)
      #  assert int(e.current_idle_duration.rstrip("s")) < initial_idle
        assert int(e.current_running_duration.rstrip("s")) < initial_runtime

    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name=f"workspaces/{workspace_id}/daiEngines/{engine_id}", allow_missing=True
        )
