from typing import Dict
from typing import List
from typing import Optional

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.exception import ApiException
from h2o_engine_manager.clients.internal_dai_version.mapper import (
    build_internal_dai_version_name,
)
from h2o_engine_manager.clients.internal_dai_version.mapper import (
    from_api_internal_dai_version_to_custom,
)
from h2o_engine_manager.clients.internal_dai_version.mapper import (
    from_custom_internal_dai_version_to_api_resource,
)
from h2o_engine_manager.clients.internal_dai_version.page import InternalDAIVersionsPage
from h2o_engine_manager.clients.internal_dai_version.token_api_client import (
    TokenApiInternalDAIVersionClient,
)
from h2o_engine_manager.clients.internal_dai_version.version import InternalDAIVersion
from h2o_engine_manager.gen.internal_dai_version_service import (
    ApiException as GenInternalDAIVersionApiException,
)
from h2o_engine_manager.gen.internal_dai_version_service.api.internal_dai_version_service_api import (
    InternalDAIVersionServiceApi,
)
from h2o_engine_manager.gen.internal_dai_version_service.configuration import (
    Configuration as InternalDAIVersionConfiguration,
)
from h2o_engine_manager.gen.internal_dai_version_service.model.v1_internal_dai_version import (
    V1InternalDAIVersion,
)


class InternalDAIVersionClient:
    """InternalDAIVersionClient manages InternalDAIVersions."""

    def __init__(
        self,
        connection_config: ConnectionConfig,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes InternalDAIVersionClient.

        Args:
            connection_config (ConnectionConfig): AIEM connection configuration object.
            verify_ssl: Set to False to disable SSL certificate verification.
            ssl_ca_cert: Path to a CA cert bundle with certificates of trusted CAs.
        """

        configuration_internal_dai_version = InternalDAIVersionConfiguration(
            host=connection_config.aiem_url
        )
        configuration_internal_dai_version.verify_ssl = verify_ssl
        configuration_internal_dai_version.ssl_ca_cert = ssl_ca_cert

        with TokenApiInternalDAIVersionClient(
            configuration_internal_dai_version, connection_config.token_provider
        ) as api_dai_version_client:
            self.gen_api_client = InternalDAIVersionServiceApi(api_dai_version_client)

    def create_version(
        self,
        internal_dai_version_id: str,
        image: str,
        image_pull_policy: ImagePullPolicy = ImagePullPolicy.IMAGE_PULL_POLICY_UNSPECIFIED,
        image_pull_secrets: List[str] = [],
        aliases: List[str] = [],
        gpu_resource_name: str = "",
        data_directory_storage_class: str = "",
        annotations: Dict[str, str] = {},
        deprecated: bool = False,
    ) -> InternalDAIVersion:
        """
        Create InternalDAIVersion.

        Args:
            internal_dai_version_id: version identifier. Must be in semver format.
                More than three segments are supported. For example "1.10.3" or "1.10.3.1".
            image: Name of the Docker image when using this version.
            image_pull_policy: Image pull policy applied when using this version.
            image_pull_secrets: List of references to k8s secrets that can be used for pulling
                an image of this version from a private container image registry or repository.
            aliases: Aliases of this version. For example ["latest"].
            gpu_resource_name: K8s GPU resource name. For example: "nvidia.com/gpu" or "amd.com/gpu".
            data_directory_storage_class: Name of the storage class used by Driverless AI when using this version.
            annotations: Additional arbitrary metadata associated with this version.
            deprecated: Indicates whether this version is deprecated.

        Returns:
            Created InternalDAIVersion.
        """

        api_version = V1InternalDAIVersion(
            image=image,
            image_pull_policy=image_pull_policy.to_idaiv_api_image_pull_policy(),
            image_pull_secrets=image_pull_secrets,
            aliases=aliases,
            gpu_resource_name=gpu_resource_name,
            data_directory_storage_class=data_directory_storage_class,
            annotations=annotations,
            deprecated=deprecated,
        )

        created_api_version = None
        exc = None

        try:
            created_api_version = self.gen_api_client.internal_dai_version_service_create_internal_dai_version(
                internal_dai_version_id=internal_dai_version_id,
                internal_dai_version=api_version,
            ).internal_dai_version
        except GenInternalDAIVersionApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return from_api_internal_dai_version_to_custom(api_internal_dai_version=created_api_version)

    def get_version(self, internal_dai_version_id: str) -> InternalDAIVersion:
        """
        Get InternalDAIVersion.

        Args:
            internal_dai_version_id: resource ID of InternalDAIVersion

        Returns:
            InternalDAIVersion
        """
        exc = None
        api_version = None

        try:
            api_version = self.gen_api_client.internal_dai_version_service_get_internal_dai_version(
                name=build_internal_dai_version_name(internal_dai_version_id=internal_dai_version_id),
            ).internal_dai_version
        except GenInternalDAIVersionApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return from_api_internal_dai_version_to_custom(api_internal_dai_version=api_version)

    def list_versions(
        self,
        page_size: int = 0,
        page_token: str = "",
    ) -> InternalDAIVersionsPage:
        """
        List InternalDAIVersions.

        Args:
            page_size: Maximum number of InternalDAIVersions to return in a response.
                If unspecified (or set to 0), at most 50 InternalDAIVersions will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token: Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the InternalDAIVersionsPage.

        Returns:
            Page of InternalDAIVersions
        """
        exc = None
        list_response = None

        try:
            list_response = (
                self.gen_api_client.internal_dai_version_service_list_internal_dai_versions(
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except GenInternalDAIVersionApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return InternalDAIVersionsPage(list_response)

    def list_all_versions(self) -> List[InternalDAIVersion]:
        """
        List all InternalDAIVersions.

        Returns:
            InternalDAIVersions
        """
        all_versions: List[InternalDAIVersion] = []
        next_page_token = ""
        while True:
            versions_list = self.list_versions(
                page_size=0,
                page_token=next_page_token,
            )
            all_versions = all_versions + versions_list.internal_dai_versions
            next_page_token = versions_list.next_page_token
            if next_page_token == "":
                break

        return all_versions

    def update_version(
        self,
        internal_dai_version: InternalDAIVersion,
        update_mask: str = "*"
    ) -> InternalDAIVersion:
        """
        Update InternalDAIVersion.

        Args:
            internal_dai_version: InternalDAIVersion with to-be-updated values.
            update_mask: Comma separated paths referencing which fields to update.
                Update mask must be non-empty.
                Allowed field paths are: {"aliases", "deprecated", "image", "image_pull_policy", "image_pull_secrets",
                "gpu_resource_name", "data_directory_storage_class", "annotations"}.

        Returns:
            Updated InternalDAIVersion
        """

        exc = None
        updated_api_version = None

        try:
            updated_api_version = self.gen_api_client.internal_dai_version_service_update_internal_dai_version(
                internal_dai_version_name=internal_dai_version.name,
                update_mask=update_mask,
                internal_dai_version=from_custom_internal_dai_version_to_api_resource(internal_dai_version),
            ).internal_dai_version
        except GenInternalDAIVersionApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return from_api_internal_dai_version_to_custom(api_internal_dai_version=updated_api_version)

    def delete_version(self, internal_dai_version_id: str) -> None:
        """
        Delete InternalDAIVersion.

        Args:
            internal_dai_version_id: ID of to-be-deleted InternalDAIVersion
        """

        exc = None

        try:
            self.gen_api_client.internal_dai_version_service_delete_internal_dai_version(
                name=build_internal_dai_version_name(internal_dai_version_id=internal_dai_version_id)
            )
        except GenInternalDAIVersionApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc
