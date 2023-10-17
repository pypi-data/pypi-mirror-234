import pprint

from h2o_engine_manager.clients.h2o_version.mapper import api_to_custom
from h2o_engine_manager.gen.h2o_version_service.model.v1_list_h2_o_versions_response import (
    V1ListH2OVersionsResponse,
)


class H2OVersionsPage:
    """Class represents a list of H2OVersions together with a next_page_token
    and a total_size for listing all H2OVersions."""

    def __init__(self, list_api_response: V1ListH2OVersionsResponse) -> None:
        generated_h2o_versions = list_api_response.h2o_versions
        self.h2o_versions = []
        for api_h2o_version in generated_h2o_versions:
            self.h2o_versions.append(api_to_custom(api_h2o_version))

        self.next_page_token = list_api_response.next_page_token
        self.total_size = list_api_response.total_size

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
