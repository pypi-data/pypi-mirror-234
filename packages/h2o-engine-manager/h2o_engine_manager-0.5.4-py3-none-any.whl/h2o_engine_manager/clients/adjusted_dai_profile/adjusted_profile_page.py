import pprint

from h2o_engine_manager.clients.adjusted_dai_profile.adjusted_profile import (
    from_api_object,
)
from h2o_engine_manager.gen.adjusted_dai_profile_service.model.v1_list_adjusted_dai_profiles_response import (
    V1ListAdjustedDAIProfilesResponse,
)


class AdjustedDAIProfilesPage:
    """Class represents a list of AdjustedDAIProfile objects together with a
    next_page_token and a total_size used for listing Adjusted DAI profiles."""

    def __init__(
            self, list_api_response: V1ListAdjustedDAIProfilesResponse
    ) -> None:
        api_profiles = list_api_response.adjusted_dai_profiles
        self.adjusted_profiles = []
        for api_profile in api_profiles:
            self.adjusted_profiles.append(
                from_api_object(
                    api_profile=api_profile
                )
            )

        self.next_page_token = list_api_response.next_page_token
        self.total_size = list_api_response.total_size

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
