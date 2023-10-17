import os
import subprocess

import pytest


@pytest.mark.parametrize(
    ["file_name", "err"],
    [
        ("invalid_version_format.yaml", "invalid version name:"),
        ("repeated_alias.yaml", "unique constraint violation:"),
        ("alias_and_version_conflict.yaml", "unique constraint violation:"),
        ("unsupported_version.yaml", "invalid version:"),
    ],
)
def test_dai_versions_validation(file_name, err):
    dai_version_namespace = os.getenv("TEST_K8S_SYSTEM_NAMESPACE")
    file_path = os.path.join(
        os.path.dirname(__file__), "test_data", "invalid_dai_versions", file_name
    )

    try:
        # When
        cmd = [
            "kubectl",
            "apply",
            "-f",
            file_path,
            f"--namespace={dai_version_namespace}",
        ]
        completed_process = subprocess.run(cmd, stderr=subprocess.PIPE)

        # Then
        assert completed_process.returncode != 0
        err_msg = f'admission webhook "validate.v1alpha1.driverlessaiversion.engine.h2o.ai" denied the request: {err}'
        assert err_msg in completed_process.stderr.decode(encoding="utf-8")
    finally:
        # Clean up after every run
        cmd = [
            "kubectl",
            "delete",
            "-f",
            file_path,
            f"--namespace={dai_version_namespace}",
            "--ignore-not-found=true",
        ]
        subprocess.run(cmd, check=True)


@pytest.mark.parametrize(
    ["file_name", "err"],
    [
        (
            "invalid-cpu-constraint.yaml",
            "invalid constraint: cpu.min must be > 0, current value: 0",
        ),
        (
            "invalid-gpu-constraint.yaml",
            "invalid constraint: gpu.default must be >= 0, current value: -1",
        ),
        (
            "invalid-max-idle-duration-constraint.yaml",
            "invalid constraint: maxIdleDuration.min must be >= 0s, current value: -1s",
        ),
    ],
)
def test_dai_setup_validation(file_name, err):
    dai_setup_namespace = os.getenv("TEST_K8S_SYSTEM_NAMESPACE")
    file_path = os.path.join(
        os.path.dirname(__file__), "test_data", "invalid_dai_setups", file_name
    )

    try:
        # When
        cmd = [
            "kubectl",
            "apply",
            "-f",
            file_path,
            f"--namespace={dai_setup_namespace}",
        ]
        completed_process = subprocess.run(cmd, stderr=subprocess.PIPE)

        # Then
        assert completed_process.returncode != 0
        err_msg = f'admission webhook "validate.v1alpha1.driverlessaisetup.engine.h2o.ai" denied the request: {err}'
        assert err_msg in completed_process.stderr.decode(encoding="utf-8")
    finally:
        # Clean up after every run
        cmd = [
            "kubectl",
            "delete",
            "-f",
            file_path,
            f"--namespace={dai_setup_namespace}",
            "--ignore-not-found=true",
        ]
        subprocess.run(cmd, check=True)


def test_sw_pod_with_no_labels_is_created():
    notebook_namespace = os.getenv("TEST_K8S_NOTEBOOK_NAMESPACE")
    file_path = os.path.join(
        os.path.dirname(__file__), "test_data", "sw_pods_creation", "no_labels.yaml"
    )

    try:
        # When
        cmd = ["kubectl", "apply", "-f", file_path, f"--namespace={notebook_namespace}"]
        completed_process = subprocess.run(cmd, stderr=subprocess.PIPE)

        # Then
        assert completed_process.returncode == 0
    finally:
        # Clean up after every run
        cmd = [
            "kubectl",
            "delete",
            "-f",
            file_path,
            f"--namespace={notebook_namespace}",
            "--ignore-not-found=true",
            "--grace-period=0",
            "--force",
        ]
        subprocess.run(cmd, check=True)


def test_sw_pod_creation_with_invalid_label_fails():
    notebook_namespace = os.getenv("TEST_K8S_NOTEBOOK_NAMESPACE")
    file_path = os.path.join(
        os.path.dirname(__file__),
        "test_data",
        "sw_pods_creation",
        "unwanted_label.yaml",
    )

    try:
        # When
        cmd = ["kubectl", "apply", "-f", file_path, f"--namespace={notebook_namespace}"]
        completed_process = subprocess.run(cmd, stderr=subprocess.PIPE)

        # Then
        assert completed_process.returncode != 0
        err = "the pod contains unwanted label"
        err_msg = f'admission webhook "validate.v1alpha1.sparklingwaterpods.engine.h2o.ai" denied the request: {err}'

        assert err_msg in completed_process.stderr.decode(encoding="utf-8")
    finally:
        # Clean up after every run
        cmd = [
            "kubectl",
            "delete",
            "-f",
            file_path,
            f"--namespace={notebook_namespace}",
            "--ignore-not-found=true",
        ]
        subprocess.run(cmd, check=True)
