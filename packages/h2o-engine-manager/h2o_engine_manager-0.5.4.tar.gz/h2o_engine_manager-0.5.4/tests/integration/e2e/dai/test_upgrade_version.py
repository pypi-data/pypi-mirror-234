import http
import time

import pytest

from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from h2o_engine_manager.clients.exception import ApiException
from tests.integration.api.dai.create_dai_request import CreateDAIEngineRequest
from tests.integration.api.dai.create_dai_request import create_dai_from_request


# Upgrade version test must be performed in tests
# that run also operator because the engine needs to change states.
@pytest.mark.timeout(180)
def test_upgrade_version(dai_client):
    workspace_id = "upgrade-dai-version"
    engine_id = "e1"
    req = CreateDAIEngineRequest(
        workspace_id=workspace_id, engine_id=engine_id, version="1.10.4"
    )
    eng = create_dai_from_request(dai_client, req)
    try:
        # Only stopped engine can be upgraded.
        assert eng.state != DAIEngineState.STATE_PAUSED
        with pytest.raises(ApiException) as exc:
            eng.upgrade_version(new_version="1.10.5-mock")
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST

        eng.pause()
        eng.wait()

        # Only available version can be used for upgrade.
        with pytest.raises(ApiException) as exc:
            eng.upgrade_version(new_version="non-existing-version")
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST

        # Can upgrade only to newer version.
        with pytest.raises(ApiException) as exc:
            eng.upgrade_version(new_version="1.10.4")
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST

        eng.upgrade_version(new_version="1.10.5-mock")
        assert eng.version == "1.10.5-mock"
        # Upgrading version is also a form of update -> update_time should be set.
        ut = eng.update_time
        assert ut is not None

        # update_time precision is one second,
        # need to wait at least one second for correct later comparison
        time.sleep(1)

        # Alias can be used for upgrade as well.
        eng.upgrade_version(new_version="latest")
        assert eng.version == "1.10.6.1"
        assert ut != eng.update_time
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )
