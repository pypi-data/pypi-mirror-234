from h2o_engine_manager.clients.dai_version.dai_version import DAIVersion
from h2o_engine_manager.gen.dai_version_service.model.v1_dai_version import V1DAIVersion


def api_to_custom(api_dai_version: V1DAIVersion) -> DAIVersion:
    """
    Map generated DAIVersion object into custom DAIVersion object.

    Args:
        api_dai_version: generated DAIVersion object

    Returns:
        mapped DAIVersion object
    """
    return DAIVersion(
        version=api_dai_version.version,
        aliases=api_dai_version.aliases,
        deprecated=api_dai_version.deprecated,
        annotations=api_dai_version.annotations,
    )
