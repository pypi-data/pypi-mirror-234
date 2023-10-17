from typing import List
from typing import Optional

from h2o_engine_manager.clients.adjusted_dai_profile.adjusted_profile import (
    AdjustedDAIProfile,
)
from h2o_engine_manager.clients.adjusted_dai_profile.adjusted_profile import (
    from_api_object,
)
from h2o_engine_manager.clients.adjusted_dai_profile.adjusted_profile_page import (
    AdjustedDAIProfilesPage,
)
from h2o_engine_manager.clients.adjusted_dai_profile.token_api_client import (
    TokenApiClient,
)
from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.exception import ApiException
from h2o_engine_manager.gen.adjusted_dai_profile_service import (
    ApiException as AdjustedDAIProfileApiException,
)
from h2o_engine_manager.gen.adjusted_dai_profile_service.api.adjusted_dai_profile_service_api import (
    AdjustedDAIProfileServiceApi,
)
from h2o_engine_manager.gen.adjusted_dai_profile_service.configuration import (
    Configuration,
)


class AdjustedDAIProfileClient:
    """AdjustedDAIProfileClient manages Adjusted Driverless AI profiles."""

    def __init__(
            self,
            connection_config:
            ConnectionConfig,
            verify_ssl: bool = True,
            ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes AdjustedDAIProfileClient.

        Args:
            connection_config (ConnectionConfig): AIEM connection configuration object.
            verify_ssl: Set to False to disable SSL certificate verification.
            ssl_ca_cert: Path to a CA cert bundle with certificates of trusted CAs.
        """

        configuration_dai_version = Configuration(
            host=connection_config.aiem_url
        )
        configuration_dai_version.verify_ssl = verify_ssl
        configuration_dai_version.ssl_ca_cert = ssl_ca_cert

        with TokenApiClient(
                configuration_dai_version, connection_config.token_provider
        ) as api_client:
            self.service_api = AdjustedDAIProfileServiceApi(api_client)

    def get_adjusted_profile(self, workspace_id: str, profile_id: str) -> AdjustedDAIProfile:
        """Returns a specific profile adjusted for a workspace.

        Args:
            workspace_id (str): The ID of a workspace.
            profile_id (str): The ID of an profile.

        Returns:
            AdjustedDAIProfile: Adjusted Driverless AI profile.
        """

        exc = None
        api_profile = None

        try:
            api_profile = (
                self.service_api.adjusted_dai_profile_service_get_adjusted_dai_profile(
                    name=f"workspaces/{workspace_id}/adjustedDAIProfiles/{profile_id}"
                ).adjusted_dai_profile
            )
        except AdjustedDAIProfileApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return from_api_object(
            api_profile=api_profile
        )

    def list_adjusted_profiles(
            self,
            workspace_id: str,
            page_size: int = 0,
            page_token: str = "",
    ) -> AdjustedDAIProfilesPage:
        """Returns a list of adjusted profiles.

        Args:
            workspace_id (str): The ID of a workspace in which adjusted profiles will be listed.
            page_size (int, optional): Maximum number of AdjustedDAIProfiles to return in a response.
                If unspecified (or set to 0), at most 50 AdjustedDAIProfiles will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str, optional): Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the AdjustedDAIProfilesPage.

        Returns:
            AdjustedDAIProfilesPage: A list of Adjusted Driverless AI profiles together with a next_page_token for the next page.
        """

        exc = None
        api_response = None

        try:
            api_response = (
                self.service_api.adjusted_dai_profile_service_list_adjusted_dai_profiles(
                    parent=f"workspaces/{workspace_id}",
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except AdjustedDAIProfileApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return AdjustedDAIProfilesPage(
            list_api_response=api_response
        )

    def list_all_adjusted_profiles(self, workspace_id: str,) -> List[AdjustedDAIProfile]:
        """Returns a list of all adjusted profiles.

        Args:
            workspace_id (str): The ID of a workspace in which adjusted profiles will be listed.

        Returns:
            List[AdjustedDAIProfile]: A list of Adjusted Driverless AI profiles.
        """

        all_profiles: List[AdjustedDAIProfile] = []
        next_page_token = ""
        while True:
            profiles_list = self.list_adjusted_profiles(
                workspace_id=workspace_id,
                page_size=0,
                page_token=next_page_token,
            )
            all_profiles = all_profiles + profiles_list.adjusted_profiles
            next_page_token = profiles_list.next_page_token
            if next_page_token == "":
                break

        return all_profiles
