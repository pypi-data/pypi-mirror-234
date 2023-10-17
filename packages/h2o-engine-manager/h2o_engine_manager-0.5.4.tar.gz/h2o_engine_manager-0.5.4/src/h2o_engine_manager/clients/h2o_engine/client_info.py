import h2o_authn

from h2o_engine_manager.gen.h2o_engine_service.api.h2_o_engine_service_api import (
    H2OEngineServiceApi,
)


class ClientInfo:
    """ClientInfo is a utility class grouping client-related data."""

    def __init__(
        self,
        url: str,
        token_provider: h2o_authn.TokenProvider,
        api_instance: H2OEngineServiceApi,
    ):
        """Initialize ClientInfo.

        Args:
            url (str): URL of the AIEM server.
            token_provider (h2o_authn.TokenProvider): Token provider.
            api_instance (H2OEngineServiceApi): Instance of the generated H2OEngine service API client.
        """
        self.url = url
        self.token_provider = token_provider
        self.api_instance = api_instance
