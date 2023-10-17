from typing import List
from typing import Optional

from h2o_engine_manager.clients.connection_config import ConnectionConfig
from h2o_engine_manager.clients.exception import ApiException
from h2o_engine_manager.clients.h2o_version.h2o_version import H2OVersion
from h2o_engine_manager.clients.h2o_version.page import H2OVersionsPage
from h2o_engine_manager.clients.h2o_version.token_api_client import (
    TokenApiH2OVersionClient,
)
from h2o_engine_manager.gen.h2o_version_service import ApiException as GenApiException
from h2o_engine_manager.gen.h2o_version_service.api.h2_o_version_service_api import (
    H2OVersionServiceApi,
)
from h2o_engine_manager.gen.h2o_version_service.configuration import (
    Configuration as H2OVersionConfiguration,
)


class H2OVersionClient:
    """H2OVersionClient manages H2O versions."""

    def __init__(
        self,
        connection_config: ConnectionConfig,
        verify_ssl: bool = True,
        ssl_ca_cert: Optional[str] = None,
    ):
        """Initializes H2OVersionClient.

        Args:
            connection_config (ConnectionConfig): AIEM connection configuration object.
            verify_ssl: Set to False to disable SSL certificate verification.
            ssl_ca_cert: Path to a CA cert bundle with certificates of trusted CAs.
        """

        configuration_h2o_version = H2OVersionConfiguration(
            host=connection_config.aiem_url
        )
        configuration_h2o_version.verify_ssl = verify_ssl
        configuration_h2o_version.ssl_ca_cert = ssl_ca_cert

        with TokenApiH2OVersionClient(
            configuration_h2o_version, connection_config.token_provider
        ) as api_h2o_version_client:
            self.api_version_instance = H2OVersionServiceApi(api_h2o_version_client)

    def list_versions(
        self,
        page_size: int = 0,
        page_token: str = "",
        order_by: str = "",
        filter: str = "",
    ) -> H2OVersionsPage:
        exc = None
        list_response = None

        try:
            list_response = (
                self.api_version_instance.h2_o_version_service_list_h2_o_versions(
                    page_size=page_size,
                    page_token=page_token,
                    order_by=order_by,
                    filter=filter,
                )
            )
        except GenApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return H2OVersionsPage(list_response)

    def list_all_versions(
        self, order_by: str = "", filter: str = ""
    ) -> List[H2OVersion]:
        all_versions: List[H2OVersion] = []
        next_page_token = ""
        while True:
            versions_list = self.list_versions(
                page_size=0,
                page_token=next_page_token,
                order_by=order_by,
                filter=filter,
            )
            all_versions = all_versions + versions_list.h2o_versions
            next_page_token = versions_list.next_page_token
            if next_page_token == "":
                break

        return all_versions
