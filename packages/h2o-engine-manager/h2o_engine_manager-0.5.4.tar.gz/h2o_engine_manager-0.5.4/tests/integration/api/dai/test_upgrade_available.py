import pytest

from tests.integration.api.dai.create_dai_request import CreateDAIEngineRequest
from tests.integration.api.dai.create_dai_request import create_dai_from_request


@pytest.mark.parametrize(
    ["engine_id", "version", "want_available"],
    [("e1", "1.10.6", True), ("e2", "1.10.6.1-alpha", True), ("e3", "1.10.6.1", False)],
    ids=[
        "Engine created with an older version has upgrade available",
        "-alpha version is not recognized as latest",
        "latest version does not have an upgrade",
    ],
)
@pytest.mark.timeout(180)
def test_upgrade_available(dai_client, engine_id, version, want_available):
    workspace_id = "upgrade-available-dai"

    req = CreateDAIEngineRequest(
        workspace_id=workspace_id, engine_id=engine_id, version=version
    )
    eng = create_dai_from_request(dai_client, req)
    try:
        assert eng.upgrade_available == want_available
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )
