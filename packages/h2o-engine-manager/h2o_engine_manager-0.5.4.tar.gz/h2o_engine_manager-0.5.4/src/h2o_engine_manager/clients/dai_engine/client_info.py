from typing import Callable

from h2o_engine_manager.gen.dai_engine_service.api.dai_engine_service_api import (
    DAIEngineServiceApi,
)


class ClientInfo:
    """ClientInfo is a utility class grouping client-related data."""

    def __init__(
        self,
        url: str,
        token_provider: Callable[[], str],
        api_instance: DAIEngineServiceApi,
    ):
        """Initialize ClientInfo.

        Args:
            url (str): URL of the AIEM server.
            token_provider (Callable[[], str]): Token provider.
            api_instance (DAIEngineServiceApi): Instance of the generated DAIEngine service API client.
        """
        self.url = url
        self.token_provider = token_provider
        self.api_instance = api_instance
