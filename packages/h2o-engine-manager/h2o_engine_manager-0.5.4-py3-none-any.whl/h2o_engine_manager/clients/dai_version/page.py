import pprint

from h2o_engine_manager.clients.dai_version.mapper import api_to_custom
from h2o_engine_manager.gen.dai_version_service.model.v1_list_dai_versions_response import (
    V1ListDAIVersionsResponse,
)


class DAIVersionsPage:
    """Class represents a list of DAIVersions together with a next_page_token
    and a total_size for listing all DAIVersions."""

    def __init__(self, list_api_response: V1ListDAIVersionsResponse) -> None:
        generated_dai_versions = list_api_response.dai_versions
        self.dai_versions = []
        for api_dai_version in generated_dai_versions:
            self.dai_versions.append(api_to_custom(api_dai_version))

        self.next_page_token = list_api_response.next_page_token
        self.total_size = list_api_response.total_size

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
