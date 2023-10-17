from typing import Dict
from typing import List
from typing import Optional

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.exception import ApiException
from h2o_engine_manager.clients.internal_h2o_version.mapper import (
    build_internal_h2o_version_name,
)
from h2o_engine_manager.clients.internal_h2o_version.mapper import (
    from_api_internal_h2o_version_to_custom,
)
from h2o_engine_manager.clients.internal_h2o_version.mapper import (
    from_custom_internal_h2o_version_to_api_resource,
)
from h2o_engine_manager.clients.internal_h2o_version.page import InternalH2OVersionsPage
from h2o_engine_manager.clients.internal_h2o_version.token_api_client import (
    TokenApiInternalH2OVersionClient,
)
from h2o_engine_manager.clients.internal_h2o_version.version import InternalH2OVersion
from h2o_engine_manager.gen.internal_h2o_version_service import (
    ApiException as GenInternalH2OVersionApiException,
)
from h2o_engine_manager.gen.internal_h2o_version_service.api.internal_h2_o_version_service_api import (
    InternalH2OVersionServiceApi,
)
from h2o_engine_manager.gen.internal_h2o_version_service.configuration import (
    Configuration as InternalH2OVersionConfiguration,
)
from h2o_engine_manager.gen.internal_h2o_version_service.model.v1_internal_h2_o_version import (
    V1InternalH2OVersion,
)


class InternalH2OVersionClient:
    """InternalH2OVersionClient manages InternalH2OVersions."""

    def __init__(
        self,
        connection_config: ConnectionConfig,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes InternalH2OVersionClient.

        Args:
            connection_config (ConnectionConfig): AIEM connection configuration object.
            verify_ssl: Set to False to disable SSL certificate verification.
            ssl_ca_cert: Path to a CA cert bundle with certificates of trusted CAs.
        """

        configuration_internal_h2o_version = InternalH2OVersionConfiguration(
            host=connection_config.aiem_url
        )
        configuration_internal_h2o_version.verify_ssl = verify_ssl
        configuration_internal_h2o_version.ssl_ca_cert = ssl_ca_cert

        with TokenApiInternalH2OVersionClient(
            configuration_internal_h2o_version, connection_config.token_provider
        ) as api_h2o_version_client:
            self.gen_api_client = InternalH2OVersionServiceApi(api_h2o_version_client)

    def create_version(
        self,
        internal_h2o_version_id: str,
        image: str,
        image_pull_policy: ImagePullPolicy = ImagePullPolicy.IMAGE_PULL_POLICY_UNSPECIFIED,
        image_pull_secrets: List[str] = [],
        aliases: List[str] = [],
        gpu_resource_name: str = "",
        annotations: Dict[str, str] = {},
        deprecated: bool = False,
    ) -> InternalH2OVersion:
        """
        Create InternalH2OVersion.

        Args:
            internal_h2o_version_id: version identifier. Must be in semver format.
                More than three segments are supported. For example "3.42.0.3".
            image: Name of the Docker image when using this version.
            image_pull_policy: Image pull policy applied when using this version.
            image_pull_secrets: List of references to k8s secrets that can be used for pulling
                an image of this version from a private container image registry or repository.
            aliases: Aliases of this version. For example ["latest"].
            gpu_resource_name: K8s GPU resource name. For example: "nvidia.com/gpu" or "amd.com/gpu".
            annotations: Additional arbitrary metadata associated with this version.
            deprecated: Indicates whether this version is deprecated.

        Returns:
            Created InternalH2OVersion.
        """

        api_version = V1InternalH2OVersion(
            image=image,
            image_pull_policy=image_pull_policy.to_ih2ov_api_image_pull_policy(),
            image_pull_secrets=image_pull_secrets,
            aliases=aliases,
            gpu_resource_name=gpu_resource_name,
            annotations=annotations,
            deprecated=deprecated,
        )

        created_api_version = None
        exc = None

        try:
            created_api_version = self.gen_api_client.internal_h2_o_version_service_create_internal_h2_o_version(
                internal_h2o_version_id=internal_h2o_version_id,
                internal_h2o_version=api_version,
            ).internal_h2o_version
        except GenInternalH2OVersionApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return from_api_internal_h2o_version_to_custom(api_internal_h2o_version=created_api_version)

    def get_version(self, internal_h2o_version_id: str) -> InternalH2OVersion:
        """
        Get InternalH2OVersion.

        Args:
            internal_h2o_version_id: resource ID of InternalH2OVersion

        Returns:
            InternalH2OVersion
        """
        exc = None
        api_version = None

        try:
            api_version = self.gen_api_client.internal_h2_o_version_service_get_internal_h2_o_version(
                name=build_internal_h2o_version_name(internal_h2o_version_id=internal_h2o_version_id),
            ).internal_h2o_version
        except GenInternalH2OVersionApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return from_api_internal_h2o_version_to_custom(api_internal_h2o_version=api_version)

    def list_versions(
        self,
        page_size: int = 0,
        page_token: str = "",
    ) -> InternalH2OVersionsPage:
        """
        List InternalH2OVersions.

        Args:
            page_size: Maximum number of InternalH2OVersions to return in a response.
                If unspecified (or set to 0), at most 50 InternalH2OVersions will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token: Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the InternalH2OVersionsPage.

        Returns:
            Page of InternalH2OVersions
        """
        exc = None
        list_response = None

        try:
            list_response = (
                self.gen_api_client.internal_h2_o_version_service_list_internal_h2_o_versions(
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except GenInternalH2OVersionApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return InternalH2OVersionsPage(list_response)

    def list_all_versions(self) -> List[InternalH2OVersion]:
        """
        List all InternalH2OVersions.

        Returns:
            InternalH2OVersions
        """
        all_versions: List[InternalH2OVersion] = []
        next_page_token = ""
        while True:
            versions_list = self.list_versions(
                page_size=0,
                page_token=next_page_token,
            )
            all_versions = all_versions + versions_list.internal_h2o_versions
            next_page_token = versions_list.next_page_token
            if next_page_token == "":
                break

        return all_versions

    def update_version(
        self,
        internal_h2o_version: InternalH2OVersion,
        update_mask: str = "*"
    ) -> InternalH2OVersion:
        """
        Update InternalH2OVersion.

        Args:
            internal_h2o_version: InternalH2OVersion with to-be-updated values.
            update_mask: Comma separated paths referencing which fields to update.
                Update mask must be non-empty.
                Allowed field paths are: {"aliases", "deprecated", "image", "image_pull_policy", "image_pull_secrets",
                "gpu_resource_name", "data_directory_storage_class", "annotations"}.

        Returns:
            Updated InternalH2OVersion
        """

        exc = None
        updated_api_version = None

        try:
            updated_api_version = self.gen_api_client.internal_h2_o_version_service_update_internal_h2_o_version(
                internal_h2o_version_name=internal_h2o_version.name,
                update_mask=update_mask,
                internal_h2o_version=from_custom_internal_h2o_version_to_api_resource(internal_h2o_version),
            ).internal_h2o_version
        except GenInternalH2OVersionApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return from_api_internal_h2o_version_to_custom(api_internal_h2o_version=updated_api_version)

    def delete_version(self, internal_h2o_version_id: str) -> None:
        """
        Delete InternalH2OVersion.

        Args:
            internal_h2o_version_id: ID of to-be-deleted InternalH2OVersion
        """

        exc = None

        try:
            self.gen_api_client.internal_h2_o_version_service_delete_internal_h2_o_version(
                name=build_internal_h2o_version_name(internal_h2o_version_id=internal_h2o_version_id)
            )
        except GenInternalH2OVersionApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc
