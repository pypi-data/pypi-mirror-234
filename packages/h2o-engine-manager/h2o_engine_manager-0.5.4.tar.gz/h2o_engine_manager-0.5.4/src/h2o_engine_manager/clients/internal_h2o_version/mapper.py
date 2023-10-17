from h2o_engine_manager.clients.base.image_pull_policy import (
    from_ih2ov_api_image_pull_policy_to_custom,
)
from h2o_engine_manager.clients.internal_h2o_version.version import InternalH2OVersion
from h2o_engine_manager.gen.internal_h2o_version_service.model.internal_h2_o_version_resource import (
    InternalH2OVersionResource,
)
from h2o_engine_manager.gen.internal_h2o_version_service.model.v1_internal_h2_o_version import (
    V1InternalH2OVersion,
)


def from_api_internal_h2o_version_to_custom(api_internal_h2o_version: V1InternalH2OVersion) -> InternalH2OVersion:
    """
    Map API InternalH2OVersion object into custom InternalH2OVersion object.
    Args:
        api_internal_h2o_version: generated InternalH2OVersion object
    Returns:
        mapped InternalH2OVersion object
    """
    return InternalH2OVersion(
        name=api_internal_h2o_version.name,
        version=api_internal_h2o_version.version,
        aliases=api_internal_h2o_version.aliases,
        deprecated=api_internal_h2o_version.deprecated,
        image=api_internal_h2o_version.image,
        image_pull_policy=from_ih2ov_api_image_pull_policy_to_custom(api_internal_h2o_version.image_pull_policy),
        image_pull_secrets=api_internal_h2o_version.image_pull_secrets,
        gpu_resource_name=api_internal_h2o_version.gpu_resource_name,
        annotations=api_internal_h2o_version.annotations,
    )


def from_custom_internal_h2o_version_to_api_resource(internal_h2o_version: InternalH2OVersion) -> InternalH2OVersionResource:
    """
    Map custom InternalH2OVersion to API InternalH2OVersion.
    Args:
        internal_h2o_version: InternalH2OVersion
    Returns:
        API InternalH2OVersion
    """
    return InternalH2OVersionResource(
        aliases=internal_h2o_version.aliases,
        deprecated=internal_h2o_version.deprecated,
        image=internal_h2o_version.image,
        image_pull_policy=internal_h2o_version.image_pull_policy.to_ih2ov_api_image_pull_policy(),
        image_pull_secrets=internal_h2o_version.image_pull_secrets,
        gpu_resource_name=internal_h2o_version.gpu_resource_name,
        annotations=internal_h2o_version.annotations,
    )


def build_internal_h2o_version_name(internal_h2o_version_id: str) -> str:
    """Build full resource name of InternalH2OVersion based on its ID.
    Args:
        internal_h2o_version_id: InternalH2OVersion ID.
    Returns:
        Full resource name of an InternalH2OVersion.
    """
    return f"internalH2OVersions/{internal_h2o_version_id}"
