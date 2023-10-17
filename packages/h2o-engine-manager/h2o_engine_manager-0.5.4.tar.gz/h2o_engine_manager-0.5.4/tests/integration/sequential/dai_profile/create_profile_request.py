from h2o_engine_manager.clients.dai_profile.client import DAIProfileClient
from h2o_engine_manager.clients.dai_profile.profile import DAIProfile


class CreateDAIProfileRequest:
    """
    Help class for wrapping create arguments.
    """

    profile_id: str
    cpu: int
    gpu: int
    memory_bytes: str
    storage_bytes: str
    display_name: str

    def __init__(
        self,
        profile_id: str = "profile1",
        cpu: int = 1,
        gpu: int = 0,
        memory_bytes: str = "1Gi",
        storage_bytes: str = "1Gi",
        display_name: str = "",
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.memory_bytes = memory_bytes
        self.storage_bytes = storage_bytes
        self.display_name = display_name
        self.profile_id = profile_id


def create_profile_from_request(
    client: DAIProfileClient, req: CreateDAIProfileRequest
) -> DAIProfile:
    """
    Help function for creating profile via CreateDAIProfileRequest.
    """
    return client.create_profile(
        profile_id=req.profile_id,
        cpu=req.cpu,
        gpu=req.gpu,
        memory_bytes=req.memory_bytes,
        storage_bytes=req.storage_bytes,
        display_name=req.display_name,
    )
