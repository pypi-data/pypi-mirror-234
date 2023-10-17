import pprint

from h2o_engine_manager.clients.internal_dai_version.mapper import (
    from_api_internal_dai_version_to_custom,
)
from h2o_engine_manager.gen.internal_dai_version_service.model.v1_list_internal_dai_versions_response import (
    V1ListInternalDAIVersionsResponse,
)


class InternalDAIVersionsPage:
    """Class represents a list of InternalDAIVersions together with a next_page_token
    and a total_size for listing all InternalDAIVersions."""

    def __init__(self, list_api_response: V1ListInternalDAIVersionsResponse) -> None:
        generated_internal_dai_versions = list_api_response.internal_dai_versions
        self.internal_dai_versions = []
        for api_dai_version in generated_internal_dai_versions:
            self.internal_dai_versions.append(from_api_internal_dai_version_to_custom(api_dai_version))

        self.next_page_token = list_api_response.next_page_token
        self.total_size = list_api_response.total_size

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
