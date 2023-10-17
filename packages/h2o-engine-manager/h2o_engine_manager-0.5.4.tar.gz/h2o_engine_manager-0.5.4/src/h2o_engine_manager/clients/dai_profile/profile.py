import pprint

from h2o_engine_manager.clients.convert import quantity_convertor
from h2o_engine_manager.gen.dai_profile_service.model.dai_profile_resource import (
    DAIProfileResource,
)
from h2o_engine_manager.gen.dai_profile_service.model.v1_dai_profile import V1DAIProfile


class DAIProfile:
    def __init__(
            self,
            name: str,
            display_name: str,
            cpu: int,
            gpu: int,
            memory_bytes: str,
            storage_bytes: str,

    ) -> None:
        self.name = name
        self.display_name = display_name
        self.cpu = cpu
        self.gpu = gpu
        self.memory_bytes = memory_bytes
        self.storage_bytes = storage_bytes

        self.dai_profile_id = ""

        if name:
            self.dai_profile_id = self.name.split("/")[1]

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def to_api_resource(self) -> DAIProfileResource:
        return DAIProfileResource(
            display_name=self.display_name,
            cpu=self.cpu,
            gpu=self.gpu,
            memory_bytes=quantity_convertor.quantity_to_number_str(self.memory_bytes),
            storage_bytes=quantity_convertor.quantity_to_number_str(self.storage_bytes),
        )


def from_api_object(api_profile: V1DAIProfile) -> DAIProfile:
    return DAIProfile(
        name=api_profile.name,
        display_name=api_profile.display_name,
        cpu=api_profile.cpu,
        gpu=api_profile.gpu,
        memory_bytes=quantity_convertor.number_str_to_quantity(api_profile.memory_bytes),
        storage_bytes=quantity_convertor.number_str_to_quantity(api_profile.storage_bytes),
    )
