import pprint

from h2o_engine_manager.clients.internal_h2o_version.mapper import (
    from_api_internal_h2o_version_to_custom,
)
from h2o_engine_manager.gen.internal_h2o_version_service.model.v1_list_internal_h2_o_versions_response import (
    V1ListInternalH2OVersionsResponse,
)


class InternalH2OVersionsPage:
    """Class represents a list of InternalH2OVersions together with a next_page_token
    and a total_size for listing all InternalH2OVersions."""

    def __init__(self, list_api_response: V1ListInternalH2OVersionsResponse) -> None:
        generated_internal_h2o_versions = list_api_response.internal_h2o_versions
        self.internal_h2o_versions = []
        for api_h2o_version in generated_internal_h2o_versions:
            self.internal_h2o_versions.append(from_api_internal_h2o_version_to_custom(api_h2o_version))

        self.next_page_token = list_api_response.next_page_token
        self.total_size = list_api_response.total_size

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)