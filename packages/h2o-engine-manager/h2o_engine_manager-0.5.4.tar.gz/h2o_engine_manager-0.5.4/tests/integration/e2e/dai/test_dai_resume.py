import http
import json
import os

import pytest
from kubernetes import client

from h2o_engine_manager.clients.dai_engine.dai_engine_state import DAIEngineState
from h2o_engine_manager.clients.exception import ApiException


@pytest.mark.timeout(150)
def test_dai_resume_update_config(dai_client, websocket_base_url):
    """
    White-box testing using k8s client to check that baseConfig in CRD object is updated
    during resume action (we cannot verify it directly via AIEM API as it is internal logic).
    """
    want_version = "mock"
    workspace_id = "dai-resume-update-config"
    engine_id = "e1"
    namespace = os.getenv("TEST_K8S_WORKLOADS_NAMESPACE")

    engine = dai_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        version=want_version,
        cpu=1,
        gpu=0,
        memory_bytes="1Gi",
        storage_bytes="1Gi",
        max_idle_duration="15m",
        max_running_duration="2d",
        display_name="My engine 1",
        config={"key1": "val1"},
    )

    try:
        engine.pause()
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_PAUSED.name

        # Check that baseConfig (picked parts) and custom config of the created engine is set correctly.
        kube_eng = get_kube_dai(
            workspace_id=workspace_id, engine_id=engine_id, namespace=namespace
        )
        orig_config = kube_eng["spec"]["configuration"]
        assert orig_config["override_virtual_cores"] == "1"
        assert (
            orig_config["base_url"]
            == "/workspaces/dai-resume-update-config/daiEngines/e1/"
        )
        assert orig_config["key1"] == "val1"

        # Manually update engine's baseConfig (need to access directly via k8s API).
        # Python k8s client supports only strategicMergePatch
        # (it doesn't support jsonPatch: https://github.com/kubernetes-client/python/issues/1216).
        client.CustomObjectsApi().patch_namespaced_custom_object(
            group="engine.h2o.ai",
            version="v1alpha1",
            namespace=namespace,
            plural="driverlessais",
            name=f"{workspace_id}.{engine_id}",
            body=(
                json.loads(
                    '{"spec": {"configuration":{"override_virtual_cores": "2", "base_url": "/woah/what/a/change/"}}}'
                )
            ),
        )
        # Check that baseConfig has been changed, custom config remains unchanged.
        changed_kube_eng = get_kube_dai(
            workspace_id=workspace_id, engine_id=engine_id, namespace=namespace
        )
        changed_config = changed_kube_eng["spec"]["configuration"]
        assert orig_config != changed_config
        assert changed_config["override_virtual_cores"] == "2"
        assert changed_config["base_url"] == "/woah/what/a/change/"
        assert changed_config["key1"] == "val1"

        # Resume engine.
        engine.resume()

        # Check that baseConfig (picked parts) and custom config of the created engine is set back correctly.
        resumed_kube_eng = get_kube_dai(
            workspace_id=workspace_id, engine_id=engine_id, namespace=namespace
        )
        resumed_config = resumed_kube_eng["spec"]["configuration"]
        assert orig_config == resumed_config
        assert resumed_config["override_virtual_cores"] == "1"
        assert (
            resumed_config["base_url"]
            == "/workspaces/dai-resume-update-config/daiEngines/e1/"
        )
        assert resumed_config["key1"] == "val1"

        with pytest.raises(ApiException) as exc:
            engine.update()
        assert exc.value.status == http.HTTPStatus.BAD_REQUEST
    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


PATCH_DAIVERSION__JSON = """
{
    "spec": {
        "image": "some-nonsense",
        "imagePullPolicy": "IfNotPresent",
        "imagePullSecrets": [
            {"name": "another-pull-secret-name"}
        ],
        "gpuResourceName": "amd.com/gpu",
        "dataDirectoryStorageClass": "foo"
    }
}
"""


@pytest.mark.timeout(150)
def test_dai_resume_updated_by_changed_daiversion(dai_client, websocket_base_url):
    """
    White-box testing using k8s client to check that DriverlessAI CRD object is updated
    during resume action (we cannot verify it directly via AIEM API as it is internal logic).
    """
    version_name = "1.10.5-do-not-use-me"
    workspace_id = "dai-resume-updated-by-changed-daiversion"
    engine_id = "e1"
    workloads_namespace = os.getenv("TEST_K8S_WORKLOADS_NAMESPACE")
    system_namespace = os.getenv("TEST_K8S_SYSTEM_NAMESPACE")

    engine = dai_client.create_engine(
        workspace_id=workspace_id,
        engine_id=engine_id,
        version=version_name,
        cpu=1,
        gpu=0,
        memory_bytes="1Gi",
        storage_bytes="1Gi",
        max_idle_duration="15m",
        max_running_duration="2d",
        display_name="My engine 1",
    )

    try:
        engine.pause()
        engine.wait()
        assert engine.state.name == DAIEngineState.STATE_PAUSED.name

        # Check that tested fields of the created engine is set correctly.
        kube_eng = get_kube_dai(
            workspace_id=workspace_id,
            engine_id=engine_id,
            namespace=workloads_namespace,
        )
        orig_image = kube_eng["spec"]["image"]
        orig_image_pull_policy = kube_eng["spec"]["imagePullPolicy"]
        orig_gpu_resource_name = kube_eng["metadata"]["annotations"][
            "engine.h2o.ai/gpu-resource-name"
        ]
        assert orig_image == "gcr.io/vorvan/h2oai/mockdai:latest"
        assert orig_image_pull_policy == "Always"
        assert orig_gpu_resource_name == "nvidia.com/gpu"
        # StorageClassName is not set.
        assert "pvcClassName" not in kube_eng["spec"]

        # Manually update DAIVersion k8s object (need to access directly via k8s API).
        # Python k8s client supports only strategicMergePatch
        # (it doesn't support jsonPatch: https://github.com/kubernetes-client/python/issues/1216).
        client.CustomObjectsApi().patch_namespaced_custom_object(
            group="engine.h2o.ai",
            version="v1alpha1",
            namespace=system_namespace,
            plural="driverlessaiversions",
            name=f"{version_name}",
            body=(json.loads(PATCH_DAIVERSION__JSON)),
        )

        # Double check DAIVersion has been updated correctly.
        updated_dai_version = get_kube_dai_version(
            name=version_name, namespace=system_namespace
        )
        assert updated_dai_version["spec"]["image"] == "some-nonsense"
        assert updated_dai_version["spec"]["imagePullPolicy"] == "IfNotPresent"
        assert updated_dai_version["spec"]["imagePullSecrets"] == [
            {"name": "another-pull-secret-name"}
        ]
        assert updated_dai_version["spec"]["gpuResourceName"] == "amd.com/gpu"
        assert updated_dai_version["spec"]["dataDirectoryStorageClass"] == "foo"

        # Resume engine.
        engine.resume()

        # Check that fields affected by changed DAIVersion are updated accordingly.
        resumed_kube_eng = get_kube_dai(
            workspace_id=workspace_id,
            engine_id=engine_id,
            namespace=workloads_namespace,
        )
        new_image = resumed_kube_eng["spec"]["image"]
        new_image_pull_policy = resumed_kube_eng["spec"]["imagePullPolicy"]
        new_gpu_resource_name = resumed_kube_eng["metadata"]["annotations"][
            "engine.h2o.ai/gpu-resource-name"
        ]
        assert new_image == "some-nonsense"
        assert new_image_pull_policy == "IfNotPresent"
        assert new_gpu_resource_name == "amd.com/gpu"
        # StorageClassName remains unchanged.
        assert "pvcClassName" not in kube_eng["spec"]

    finally:
        dai_client.client_info.api_instance.d_ai_engine_service_delete_dai_engine(
            name=f"workspaces/{workspace_id}/daiEngines/{engine_id}"
        )


def get_kube_dai(workspace_id: str, engine_id: str, namespace: str):
    return client.CustomObjectsApi().get_namespaced_custom_object(
        group="engine.h2o.ai",
        version="v1alpha1",
        namespace=namespace,
        plural="driverlessais",
        name=f"{workspace_id}.{engine_id}",
    )


def get_kube_dai_version(name: str, namespace: str):
    return client.CustomObjectsApi().get_namespaced_custom_object(
        group="engine.h2o.ai",
        version="v1alpha1",
        namespace=namespace,
        plural="driverlessaiversions",
        name=f"{name}",
    )
