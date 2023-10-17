import pprint
from typing import Dict
from typing import List


class H2OVersion:
    """Class represents H2O version."""

    def __init__(
        self, version: str, aliases: List[str], deprecated: bool, annotations: Dict[str, str]
    ) -> None:
        self.version = version
        self.aliases = aliases
        self.deprecated = deprecated,
        self.annotations = annotations

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
