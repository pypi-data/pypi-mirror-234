from h2o_engine_manager.clients.base.image_pull_policy import (
    from_idaiv_api_image_pull_policy_to_custom,
)
from h2o_engine_manager.clients.internal_dai_version.version import InternalDAIVersion
from h2o_engine_manager.gen.internal_dai_version_service.model.internal_dai_version_resource import (
    InternalDAIVersionResource,
)
from h2o_engine_manager.gen.internal_dai_version_service.model.v1_internal_dai_version import (
    V1InternalDAIVersion,
)


def from_api_internal_dai_version_to_custom(api_internal_dai_version: V1InternalDAIVersion) -> InternalDAIVersion:
    """
    Map API InternalDAIVersion object into custom InternalDAIVersion object.

    Args:
        api_internal_dai_version: generated InternalDAIVersion object

    Returns:
        mapped InternalDAIVersion object
    """
    return InternalDAIVersion(
        name=api_internal_dai_version.name,
        version=api_internal_dai_version.version,
        aliases=api_internal_dai_version.aliases,
        deprecated=api_internal_dai_version.deprecated,
        image=api_internal_dai_version.image,
        image_pull_policy=from_idaiv_api_image_pull_policy_to_custom(api_internal_dai_version.image_pull_policy),
        image_pull_secrets=api_internal_dai_version.image_pull_secrets,
        gpu_resource_name=api_internal_dai_version.gpu_resource_name,
        data_directory_storage_class=api_internal_dai_version.data_directory_storage_class,
        annotations=api_internal_dai_version.annotations,
    )


def from_custom_internal_dai_version_to_api_resource(
    internal_dai_version: InternalDAIVersion
) -> InternalDAIVersionResource:
    """
    Map custom InternalDAIVersion to API InternalDAIVersion.

    Args:
        internal_dai_version: InternalDAIVersion
    Returns:
        API InternalDAIVersion
    """

    # Cannot set version or name parameter, because they are read-only.
    return InternalDAIVersionResource(
        aliases=internal_dai_version.aliases,
        deprecated=internal_dai_version.deprecated,
        image=internal_dai_version.image,
        image_pull_policy=internal_dai_version.image_pull_policy.to_idaiv_api_image_pull_policy(),
        image_pull_secrets=internal_dai_version.image_pull_secrets,
        gpu_resource_name=internal_dai_version.gpu_resource_name,
        data_directory_storage_class=internal_dai_version.data_directory_storage_class,
        annotations=internal_dai_version.annotations,
    )


def build_internal_dai_version_name(internal_dai_version_id: str) -> str:
    """Build full resource name of InternalDAIVersion based on its ID.
    Args:
        internal_dai_version_id: InternalDAIVersion ID.
    Returns:
        Full resource name of an InternalDAIVersion.
    """
    return f"internalDAIVersions/{internal_dai_version_id}"
