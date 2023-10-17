import pprint
from typing import Dict
from typing import List

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy


class InternalH2OVersion:
    """
    InternalH2OVersion represents H2OVersion with additional internal properties applied on engines when
    using this version.
    """

    def __init__(
        self,
        name: str,
        version: str,
        aliases: List[str],
        deprecated: bool,
        image: str,
        image_pull_policy: ImagePullPolicy,
        image_pull_secrets: List[str],
        gpu_resource_name: str,
        annotations: Dict[str, str],
    ) -> None:
        self.name = name
        self.version = version
        self.aliases = aliases
        self.deprecated = deprecated
        self.image = image
        self.image_pull_policy = image_pull_policy
        self.image_pull_secrets = image_pull_secrets
        self.gpu_resource_name = gpu_resource_name
        self.annotations = annotations

        self.internal_h2o_version_id = ""

        if name:
            self.internal_h2o_version_id = self.name.split("/")[1]

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)
