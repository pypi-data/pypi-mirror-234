from h2o_engine_manager.clients.h2o_version.h2o_version import H2OVersion
from h2o_engine_manager.gen.h2o_version_service.model.v1_h2_o_version import (
    V1H2OVersion,
)


def api_to_custom(api_h2o_version: V1H2OVersion) -> H2OVersion:
    """
    Map generated H2OVersion object into custom H2OVersion object.

    Args:
        api_h2o_version: generated H2OVersion object

    Returns:
        mapped H2OVersion object
    """
    return H2OVersion(
        version=api_h2o_version.version,
        aliases=api_h2o_version.aliases,
        deprecated=api_h2o_version.deprecated,
        annotations=api_h2o_version.annotations,
    )
