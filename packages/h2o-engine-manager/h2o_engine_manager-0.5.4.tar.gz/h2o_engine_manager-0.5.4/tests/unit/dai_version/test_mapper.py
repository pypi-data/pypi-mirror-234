from h2o_engine_manager.clients.dai_version.dai_version import DAIVersion
from h2o_engine_manager.clients.dai_version.mapper import api_to_custom
from h2o_engine_manager.gen.dai_version_service.model.v1_dai_version import V1DAIVersion


def test_api_to_custom():
    # Arrange
    api_object = V1DAIVersion._from_openapi_data(
        version="1.10.0", aliases=["latest", "prerelease"], deprecated=False, annotations={"key1": "val1"}
    )
    expected_custom = DAIVersion(
        version="1.10.0", aliases=["latest", "prerelease"], deprecated=False, annotations={"key1": "val1"}
    )

    # When
    custom = api_to_custom(api_object)

    # Then
    assert expected_custom.__dict__ == custom.__dict__
