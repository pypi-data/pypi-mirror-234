import asyncio
import base64
import http
import pprint
import time
from datetime import datetime
from datetime import timezone
from typing import Dict
from typing import Optional
from typing import Union

import driverlessai

from h2o_engine_manager.clients.convert import duration_convertor
from h2o_engine_manager.clients.convert import quantity_convertor
from h2o_engine_manager.clients.dai_engine.client_info import ClientInfo
from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from h2o_engine_manager.clients.dai_engine.dai_engine_state import final_states
from h2o_engine_manager.clients.dai_engine.dai_engine_state import (
    from_dai_engine_state_api_object,
)
from h2o_engine_manager.clients.exception import ApiException
from h2o_engine_manager.clients.exception import FailedEngineException
from h2o_engine_manager.clients.exception import TimeoutException
from h2o_engine_manager.gen.dai_engine_service.exceptions import (
    ApiException as GenApiException,
)
from h2o_engine_manager.gen.dai_engine_service.model.dai_engine_resource import (
    DAIEngineResource,
)
from h2o_engine_manager.gen.dai_engine_service.model.dai_engine_service_migrate_creator_request import (
    DAIEngineServiceMigrateCreatorRequest,
)
from h2o_engine_manager.gen.dai_engine_service.model.dai_engine_service_pause_dai_engine_request import (
    DAIEngineServicePauseDAIEngineRequest,
)
from h2o_engine_manager.gen.dai_engine_service.model.dai_engine_service_resume_dai_engine_request import (
    DAIEngineServiceResumeDAIEngineRequest,
)
from h2o_engine_manager.gen.dai_engine_service.model.dai_engine_service_upgrade_version_request import (
    DAIEngineServiceUpgradeVersionRequest,
)
from h2o_engine_manager.gen.dai_engine_service.model.v1_dai_engine import V1DAIEngine


class DAIEngine:
    def __init__(
        self,
        version: str,
        cpu: int,
        gpu: int,
        memory_bytes: str,
        storage_bytes: str,
        config: Dict[str, str],
        annotations: Dict[str, str],
        max_idle_duration: str,
        max_running_duration: str,
        display_name: str,
        name: str = "",
        state: DAIEngineState = DAIEngineState.STATE_UNSPECIFIED,
        creator: str = "",
        creator_display_name: str = "",
        create_time: datetime = datetime.fromtimestamp(0, tz=timezone.utc),
        update_time: datetime = None,
        delete_time: datetime = None,
        resume_time: datetime = None,
        login_url: str = "",
        api_url: str = "",
        reconciling: bool = False,
        uid: str = "",
        upgrade_available: bool = False,
        client_info: ClientInfo = None,
        current_running_duration: str = None,
        current_idle_duration: str = None,
    ) -> None:
        self.version = version
        self.cpu = cpu
        self.gpu = gpu
        self.memory_bytes = memory_bytes
        self.storage_bytes = storage_bytes
        self.config = config
        self.annotations = annotations
        self.max_idle_duration = max_idle_duration
        self.max_running_duration = max_running_duration
        self.display_name = display_name

        self.name = name
        self.state = state
        self.creator = creator
        self.creator_display_name = creator_display_name
        self.create_time = create_time
        self.update_time = update_time
        self.delete_time = delete_time
        self.resume_time = resume_time
        self.login_url = login_url
        self.api_url = api_url
        self.reconciling = reconciling
        self.uid = uid
        self.upgrade_available = upgrade_available

        self.workspace_id = ""
        self.engine_id = ""
        if name:
            self.workspace_id = self.name.split("/")[1]
            self.engine_id = self.name.split("/")[3]

        self.client_info = client_info
        self.current_running_duration = current_running_duration
        self.current_idle_duration = current_idle_duration

    def __repr__(self) -> str:
        return pprint.pformat(self.__dict__)

    def resume(self):
        """Resumes the engine and updates its data from the server response."""
        exc = None
        api_engine = None

        try:
            api_engine = (
                self.client_info.api_instance.d_ai_engine_service_resume_dai_engine(
                    name=self.name,
                    body=DAIEngineServiceResumeDAIEngineRequest(validate_only=False),
                ).dai_engine
            )
        except GenApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        self.__update_data(api_engine)

    def pause(self):
        """Pauses the engine and updates its data from the server response."""
        api_engine = None
        exc = None

        try:
            api_engine = (
                self.client_info.api_instance.d_ai_engine_service_pause_dai_engine(
                    name=self.name,
                    body=DAIEngineServicePauseDAIEngineRequest(validate_only=False),
                ).dai_engine
            )
        except GenApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        self.__update_data(api_engine)

    def delete(self, allow_missing: bool = False, validate_only: bool = False):
        """Initiates deletion of the engine from its workspace.
           Once the engine is deleted, any further action with the engine will result in an error.

        Args:
            allow_missing (bool, optional): When set to True and the DAIEngine
            is not found, then the request will succeed but no changes are made.
            validate_only(bool, optional): When set to True, request is
            validated but no changes are made.
        """

        exc = None
        api_engine = None

        try:
            api_engine = (
                self.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
                    name=self.name,
                    allow_missing=allow_missing,
                    validate_only=validate_only,
                )
            )
        except GenApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        if api_engine.dai_engine is not None:
            self.__update_data(api_engine.dai_engine)
        else:
            self.delete_time = datetime.now()
            self.state = DAIEngineState.STATE_DELETING

    def update(
        self,
        update_mask: str = "*",
        allow_missing: bool = False,
        validate_only: bool = False,
    ):
        """Updates the engine.

        Args:
            update_mask (str, optional): Comma separated paths referencing which fields to update.
                Update mask must be non-empty.

                Allowed field paths are: {"cpu", "gpu", "memory_bytes", "config", "annotations", "display_name",
                "max_idle_duration", "max_running_duration"}.
                Paths are case sensitive (must match exactly).
                Example - update only cpu: update_mask="cpu"
                Example - update only cpu and gpu: update_mask="cpu,gpu"

                To update all allowed fields, specify exactly one path with value "*", this is a default value.
            allow_missing (bool, optional): When set and the DAIEngine is not found, a new one is created.
                In this situation, `update_mask` is ignored, i.e. all fields are applied
                regardless of any provided update mask; but the update mask must be still
                present. Defaults to False.
            validate_only (bool, optional): When set, request is validated but no changes are made. Defaults to False.
        """
        updated_api_engine = None
        exc = None

        try:
            updated_api_engine = (
                self.client_info.api_instance.d_ai_engine_service_update_dai_engine(
                    dai_engine_name=self.name,
                    update_mask=update_mask,
                    dai_engine=self.to_dai_engine_resource(),
                    allow_missing=allow_missing,
                    validate_only=validate_only,
                ).dai_engine
            )
        except GenApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        self.__update_data(updated_api_engine)

    def download_logs(self) -> str:
        """Download Driverless AI logs.
        Returns:
            Driverless AI logs
        """
        exc = None
        resp = None

        try:
            resp = self.client_info.api_instance.d_ai_engine_service_download_logs(
                dai_engine=self.name, body=None
            )
        except GenApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return base64.b64decode(resp.logs.data).decode("utf-8")

    def upgrade_version(self, new_version: str):
        """Upgrade DAIEngine version.
        Args:
            new_version (str): name of the new version. Must be greater than the current version.
        Examples:
            engine.upgrade_version(new_version="1.10.3")
        """
        exc = None
        engine = None

        try:
            engine = self.client_info.api_instance.d_ai_engine_service_upgrade_version(
                dai_engine=self.name,
                body=DAIEngineServiceUpgradeVersionRequest(new_version=new_version),
            ).dai_engine
        except GenApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        self.__update_data(engine)

    def migrate_creator(self, new_creator: str):
        """Migrate creator of this DAIEngine. Admin only.
        Args:
            new_creator (str): name of an entity that becomes the new creator of the DAIEngine.
        Examples:
            engine.migrate_creator(new_creator="users/397b8c16-f4cb-41dd-a5e9-5e838edb81ab")
        """
        exc = None
        engine = None

        try:
            engine = self.client_info.api_instance.d_ai_engine_service_migrate_creator(
                dai_engine=self.name,
                body=DAIEngineServiceMigrateCreatorRequest(new_creator=new_creator),
            ).dai_engine
        except GenApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        self.__update_data(engine)

    def connect(
        self,
        verify: Union[bool, str] = True,
        backend_version_override: Optional[str] = None,
    ) -> driverlessai.Client:
        """Connect to and interact with a Driverless AI server.

        Args:
            verify (Union[bool, str], optional): when using https on the Driverless AI server, setting this to
                False will disable SSL certificates verification. A path to cert(s) can also be passed to verify, see:
                https://requests.readthedocs.io/en/master/user/advanced/#ssl-cert-verification. Defaults to True.
            backend_version_override (Optional[str], optional): version of client backend to use, overrides
                Driverless AI server version detection. Specify ``"latest"`` to get
                the most recent backend supported. In most cases the user should
                rely on Driverless AI server version detection and leave this as
                the default. Defaults to None.
        """
        if self.state is not DAIEngineState.STATE_RUNNING:
            raise RuntimeError(
                f"DAIEngine {self.name} in not in a running state. Current state: {self.state}."
            )

        # In 1.10.3 version (and prior), the connect function called after the launch (or resume), might fail
        # due to a faulty health check on the DAI server. Client initialization is retried with a 1s delay if it fails.
        max_att = 5
        for i in range(max_att):
            try:
                return driverlessai.Client(
                    address=self.api_url,
                    token_provider=self.client_info.token_provider,
                    verify=verify,
                    backend_version_override=backend_version_override,
                )
            except Exception:
                time.sleep(1)
                if i == max_att - 1:
                    raise

    def wait(self, timeout_seconds: float = None):
        """Waits for the engine to reach a final (stable) state. Final states are
           RUNNING or PAUSED. Function updates an engine every 5 seconds and
           checks its internal state. While waiting for the next update, function
           calls `time.sleep()`.

        Args:
            timeout_seconds (float, optional): Time limit in seconds for how
            long to wait. If no timeout is specified, function will be blocking
            until the waiting is finished. Potentially forever in case of an unexpected error.
            Defaults to None.
        """
        start = time.time()

        while True:
            if timeout_seconds is not None and time.time() - start > timeout_seconds:
                raise TimeoutException()

            time.sleep(5)
            if self.__is_in_final_state_and_update_exc():
                return

    async def wait_async(self, timeout_seconds: float = None):
        """Waits for an engine to reach a final (stable) state. Final states are RUNNING or PAUSED.
        Function updates an engine every 5 seconds and checks its internal state. While waiting for the next update, function calls `asyncio.sleep()`.

        Args:
            timeout_seconds (float, optional): Time limit in seconds for how
            long to wait. If no timeout is specified, function will be blocking
            until the waiting is finished. Potentially forever in case of an unexpected error.
            Defaults to None.
        """
        start = time.time()

        while True:
            if timeout_seconds is not None and time.time() - start > timeout_seconds:
                raise TimeoutException()

            await asyncio.sleep(5)
            if self.__is_in_final_state_and_update_exc():
                return

    def __is_in_final_state_and_update_exc(self) -> bool:
        exc = None
        result = None

        try:
            result = self.__is_in_final_state_and_update()
        except GenApiException as e:
            exc = ApiException(e)

        if exc:
            raise exc

        return result

    def __is_in_final_state_and_update(self) -> bool:
        """Returns True if DAIEngine is in final state. Potentially updates the calling engine as well."""
        engine = self.__get_or_none_if_not_found()
        if self.state == DAIEngineState.STATE_DELETING and engine is None:
            return True

        # Always update pythonDAIEngine with the latest APIDAIEngine.
        self.__update_data(engine.dai_engine)

        if self.__is_api_engine_in_final_state(engine):
            return True

        return False

    def __get_or_none_if_not_found(self) -> V1DAIEngine:
        """Returns engine if found, None value if not found.

        Returns:
            engine: engine or None value.
        """
        engine = None
        try:
            engine = self.client_info.api_instance.d_ai_engine_service_get_dai_engine(
                name=self.name
            )
        except GenApiException as exc:
            if exc.status == http.HTTPStatus.NOT_FOUND:
                return None
            raise exc

        return engine

    def __is_api_engine_in_final_state(self, api_engine: V1DAIEngine) -> bool:
        """Returns True if API DAIEngine is in a final state.

        Args:
            api_engine (DAIEngine): API DAIEngine

        Raises:
            FailedEngineException: Raises exception when FAILED state is observed.

        Returns:
            bool: True if final state is observed, False otherwise.
        """
        engine = from_dai_engine_api_object(
            client_info=self.client_info, api_engine=api_engine.dai_engine
        )
        if engine.state == DAIEngineState.STATE_FAILED:
            raise FailedEngineException()

        if engine.state in final_states():
            return True

        return False

    def __update_data(self, engine: V1DAIEngine):
        updated_engine = from_dai_engine_api_object(
            client_info=self.client_info, api_engine=engine
        )
        self.__dict__.update(updated_engine.__dict__)

    def to_api_object(self) -> V1DAIEngine:
        mb = None
        if self.memory_bytes is not None:
            mb = quantity_convertor.quantity_to_number_str(self.memory_bytes)

        sb = None
        if self.storage_bytes is not None:
            sb = quantity_convertor.quantity_to_number_str(self.storage_bytes)

        mid = None
        if self.max_idle_duration is not None:
            mid = duration_convertor.duration_to_seconds(self.max_idle_duration)

        mrd = None
        if self.max_running_duration is not None:
            mrd = duration_convertor.duration_to_seconds(self.max_running_duration)

        cid = None
        if self.current_idle_duration is not None:
            cid = duration_convertor.duration_to_seconds(self.current_idle_duration)

        crd = None
        if self.current_running_duration is not None:
            crd = duration_convertor.duration_to_seconds(self.current_running_duration)

        return V1DAIEngine._from_openapi_data(
            version=self.version,
            cpu=self.cpu,
            gpu=self.gpu,
            memory_bytes=mb,
            storage_bytes=sb,
            max_idle_duration=mid,
            max_running_duration=mrd,
            current_idle_duration=cid,
            current_running_duration=crd,
            display_name=self.display_name,
            name=self.name,
            state=self.state.to_api_object(),
            config=self.config,
            creator=self.creator,
            creator_display_name=self.creator_display_name,
            create_time=self.create_time,
            update_time=self.update_time,
            delete_time=self.delete_time,
            resume_time=self.resume_time,
            login_url=self.login_url,
            api_url=self.api_url,
            annotations=self.annotations,
            reconciling=self.reconciling,
            uid=self.uid,
            upgrade_available=self.upgrade_available,
        )

    def to_dai_engine_resource(self) -> DAIEngineResource:
        # DAIEngineResource cannot be instantiated with readOnly fields (e.g. creator, createTime, etc.).
        # This object is used as input for UpdateDAIEngine, so we don't need to (we should not) set readOnly fields.
        #
        # Note: Although 'state' is not generated as readOnly (the python generated code doesn't consider it readOnly),
        # it is in fact readOnly field, so we're skipping it too.

        mb = None
        if self.memory_bytes is not None:
            mb = quantity_convertor.quantity_to_number_str(self.memory_bytes)

        sb = None
        if self.storage_bytes is not None:
            sb = quantity_convertor.quantity_to_number_str(self.storage_bytes)

        mid = None
        if self.max_idle_duration is not None:
            mid = duration_convertor.duration_to_seconds(self.max_idle_duration)

        mrd = None
        if self.max_running_duration is not None:
            mrd = duration_convertor.duration_to_seconds(self.max_running_duration)

        return DAIEngineResource(
            version=self.version,
            cpu=self.cpu,
            gpu=self.gpu,
            memory_bytes=mb,
            storage_bytes=sb,
            max_idle_duration=mid,
            max_running_duration=mrd,
            display_name=self.display_name,
            config=self.config,
            annotations=self.annotations,
        )


def from_dai_engine_api_object(
    client_info: ClientInfo, api_engine: V1DAIEngine
) -> DAIEngine:
    return DAIEngine(
        version=api_engine.version,
        cpu=api_engine.cpu,
        gpu=api_engine.gpu,
        memory_bytes=quantity_convertor.number_str_to_quantity(api_engine.memory_bytes),
        storage_bytes=quantity_convertor.number_str_to_quantity(
            api_engine.storage_bytes
        ),
        config=api_engine.config,
        annotations=api_engine.annotations,
        max_idle_duration=duration_convertor.seconds_to_duration(
            api_engine.max_idle_duration
        ),
        max_running_duration=duration_convertor.seconds_to_duration(
            api_engine.max_running_duration
        ),
        display_name=api_engine.display_name,
        name=api_engine.name,
        state=from_dai_engine_state_api_object(api_engine.state),
        creator=api_engine.creator,
        creator_display_name=api_engine.creator_display_name,
        create_time=api_engine.create_time,
        update_time=api_engine.update_time,
        delete_time=api_engine.delete_time,
        resume_time=api_engine.resume_time,
        login_url=api_engine.login_url,
        api_url=api_engine.api_url,
        reconciling=api_engine.reconciling,
        uid=api_engine.uid,
        upgrade_available=api_engine.upgrade_available,
        client_info=client_info,
        current_idle_duration=duration_convertor.none_seconds_to_duration(
            api_engine.current_idle_duration
        ),
        current_running_duration=duration_convertor.none_seconds_to_duration(
            api_engine.current_running_duration
        ),
    )
