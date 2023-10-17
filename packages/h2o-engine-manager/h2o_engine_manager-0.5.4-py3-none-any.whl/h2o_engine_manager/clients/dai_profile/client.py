from typing import List
from typing import Optional

from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.connection_config import get_connection
from h2o_engine_manager.clients.convert import quantity_convertor
from h2o_engine_manager.clients.dai_profile.profile import DAIProfile
from h2o_engine_manager.clients.dai_profile.profile import from_api_object
from h2o_engine_manager.clients.dai_profile.profile_page import DAIProfilesPage
from h2o_engine_manager.clients.dai_profile.token_api_client import TokenApiClient
from h2o_engine_manager.clients.exception import ApiException
from h2o_engine_manager.gen.dai_profile_service import (
    ApiException as DAIProfileApiException,
)
from h2o_engine_manager.gen.dai_profile_service.api.dai_profile_service_api import (
    DAIProfileServiceApi,
)
from h2o_engine_manager.gen.dai_profile_service.configuration import Configuration
from h2o_engine_manager.gen.dai_profile_service.model.v1_dai_profile import V1DAIProfile


class DAIProfileClient:
    """DAIProfileClient manages DAIProfiles."""

    def __init__(
            self,
            connection_config: ConnectionConfig,
            verify_ssl: bool = True,
            ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes DAIProfileClient.
        Do not initialize manually, use `h2o_engine_manager.login()` instead.

        Args:
            connection_config (ConnectionConfig): AIEM connection configuration object.
            verify_ssl: Set to False to disable SSL certificate verification.
            ssl_ca_cert: Path to a CA cert bundle with certificates of trusted CAs.
        """

        configuration = Configuration(host=connection_config.aiem_url)
        configuration.verify_ssl = verify_ssl
        configuration.ssl_ca_cert = ssl_ca_cert

        with TokenApiClient(
                configuration, connection_config.token_provider
        ) as api_client:
            self.service_api = DAIProfileServiceApi(api_client)

    def create_profile(self,
                       profile_id: str,
                       cpu: int,
                       gpu: int,
                       memory_bytes: str,
                       storage_bytes: str,
                       display_name: str = "",
                       ) -> DAIProfile:
        """Creates Driverless AI profile.

        Args:
            profile_id (str, optional): The ID to use for the Driverless AI profile, which will become the final component of the profile's resource name.
                This value must:

                - contain 1-63 characters
                - contain only lowercase alphanumeric characters or hyphen ('-')
                - start with an alphabetic character
                - end with an alphanumeric character
            cpu (int, optional): The amount of [CPU units](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#meaning-of-cpu) set for the profile.
            gpu (int, optional): Number of nvidia.com/gpu Kubernetes resource units.
            memory_bytes (str, optional): Quantity of bytes.
                Example `8G`, `16Gi`. Detailed syntax:

                - [quantity] = [number][suffix]
                - [suffix] = [binarySI] | [decimalSI]
                - [binarySI] = Ki | Mi | Gi | Ti | Pi
                - [decimalSI] = k | M | G | T | P
            storage_bytes (str, optional): Quantity of bytes. Example `250G`, `2T`. Same syntax applies as `memory_bytes` parameter.
            display_name (str, optional): Human-readable name of the DAIProfile. Must contain at most 63 characters. Does not have to be unique.

        Returns:
            DAIProfile: Driverless AI profile.
        """

        api_profile = V1DAIProfile(
            display_name=display_name,
            cpu=cpu,
            gpu=gpu,
            memory_bytes=quantity_convertor.quantity_to_number_str(memory_bytes),
            storage_bytes=quantity_convertor.quantity_to_number_str(storage_bytes),
        )

        created_api_profile = None
        exc = None

        try:
            created_api_profile = self.service_api.d_ai_profile_service_create_dai_profile(
                dai_profile_id=profile_id,
                dai_profile=api_profile
            ).dai_profile
        except DAIProfileApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        created_profile = from_api_object(
            api_profile=created_api_profile
        )

        return created_profile

    def get_profile(self, profile_id: str) -> DAIProfile:
        """Returns a specific profile.

        Args:
            profile_id (str): The ID of an profile.

        Returns:
            DAIProfile: Driverless AI profile.
        """

        exc = None
        api_profile = None

        try:
            api_profile = (
                self.service_api.d_ai_profile_service_get_dai_profile(
                    name=f"daiProfiles/{profile_id}"
                ).dai_profile
            )
        except DAIProfileApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return from_api_object(
            api_profile=api_profile
        )

    def list_profiles(
            self,
            page_size: int = 0,
            page_token: str = "",
    ) -> DAIProfilesPage:
        """Returns a list of profiles.

        Args:
            page_size (int, optional): Maximum number of DAIProfiles to return in a response.
                If unspecified (or set to 0), at most 50 DAIProfiles will be returned.
                The maximum value is 1000; values above 1000 will be coerced to 1000.
            page_token (str, optional): Leave unset to receive the initial page.
                To list any subsequent pages use the value of 'next_page_token' returned from the DAIProfilesPage.

        Returns:
            DAIProfilesPage: A list of Driverless AI profiles together with a next_page_token for the next page.
        """

        exc = None
        api_response = None

        try:
            api_response = (
                self.service_api.d_ai_profile_service_list_dai_profiles(
                    page_size=page_size,
                    page_token=page_token,
                )
            )
        except DAIProfileApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return DAIProfilesPage(
            list_api_response=api_response
        )

    def list_all_profiles(self) -> List[DAIProfile]:
        """Returns a list of all profiles.

        Returns:
            List[DAIProfile]: A list of Driverless AI profiles.
        """

        all_profiles: List[DAIProfile] = []
        next_page_token = ""
        while True:
            profiles_list = self.list_profiles(
                page_size=0,
                page_token=next_page_token,
            )
            all_profiles = all_profiles + profiles_list.profiles
            next_page_token = profiles_list.next_page_token
            if next_page_token == "":
                break

        return all_profiles

    def update_profile(self, profile: DAIProfile, update_mask: str = "*",) -> DAIProfile:
        """Updates the profile.

        Args:
            profile (DAIProfile): The profile to be updated.
            update_mask (str, optional): Comma separated paths referencing which fields to update.
                Update mask must be non-empty.

                Allowed field paths are: {"cpu", "gpu", "memory_bytes", "storage_bytes", "display_name"}.
                Paths are case sensitive (must match exactly).
                Example - update only cpu: update_mask="cpu"
                Example - update only cpu and gpu: update_mask="cpu,gpu"

                To update all allowed fields, specify exactly one path with value "*", this is a default value.

        Returns:
            DAIProfile: An updated Driverless AI profile.
        """
        exc = None
        updated_profile = None

        api_object = profile.to_api_resource()
        try:
            updated_profile = self.service_api.d_ai_profile_service_update_dai_profile(
                dai_profile_name=profile.name,
                update_mask=update_mask,
                dai_profile=api_object,
            )
        except DAIProfileApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return from_api_object(
            api_profile=updated_profile.dai_profile
        )

    def delete_profile(self, profile_id: str) -> None:
        """Deletes a profile.

        Args:
            profile_id (str): The ID of an profile.
        """

        exc = None

        try:
            self.service_api.d_ai_profile_service_delete_dai_profile(
                name=f"daiProfiles/{profile_id}"
            )
        except DAIProfileApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

