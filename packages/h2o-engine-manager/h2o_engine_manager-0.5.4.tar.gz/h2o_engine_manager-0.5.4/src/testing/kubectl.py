import os
import subprocess

from kubernetes import client


def kubectl_apply_dir(dir_path: str, namespace: str, check: bool = True):
    """
    kubectl-apply everything in a specified directory into a specified namespace.

    Args:
        dir_path: absolute path to the directory with specs.
        namespace: k8s namespace into which apply specs.
        check: True to exit with code 1 when error occurs. False will ignore errors.
    """
    # Cannot use kubernetes library because it does not support similar functionality
    # as "kubectl apply" for CRDs (https://github.com/kubernetes-client/python/issues/740).
    # Need to run the command directly via subprocess.
    subprocess.run(
        [
            "kubectl",
            "apply",
            "-f",
            dir_path,
            "--recursive",
            f"--namespace={namespace}",
        ],
        check=check,
    )


def kubectl_delete_dir(dir_path: str, namespace: str):
    """
    kubectl-delete everything specified in a directory from a namespace.

    Args:
        dir_path: absolute path to the directory with specs.
        namespace: k8s namespace in which delete specs.
    """

    subprocess.run(
        [
            "kubectl",
            "delete",
            "-f",
            dir_path,
            "--recursive",
            f"--namespace={namespace}",
        ],
        check=True,
    )


def create_dai_license(namespace: str) -> None:
    """
    Create DAI license secret

    Args:
        namespace: namespace in which the DAI license should be created
    """
    data = {"license.sig": os.getenv("DAI_LICENSE")}
    body = client.V1Secret(
        metadata=client.V1ObjectMeta(name="dai-license"),
        type="Opaque",
        string_data=data,
    )
    client.CoreV1Api().create_namespaced_secret(namespace=namespace, body=body)


def setup_mlops_secrets(namespace: str) -> None:
    """
    Create MLOps secrets.

    Args:
        namespace: namespace in which the secrets should be created
    """

    # Gather data from existing secrets.
    ca_secret = client.CoreV1Api().read_namespaced_secret(
        "hac-mlops-dev-ca", "mlops-dev"
    )
    ca_cert = ca_secret.data["certificate"]

    client_secret = client.CoreV1Api().read_namespaced_secret(
        "hac-mlops-dev-driverless-tls-client", "mlops-dev"
    )
    client_cert = client_secret.data["certificate"]
    client_key = client_secret.data["key"]

    client.CoreV1Api().create_namespaced_secret(
        namespace,
        client.V1Secret(
            metadata=client.V1ObjectMeta(
                name=ca_secret.metadata.name, labels=ca_secret.metadata.labels
            ),
            data={"tls.crt": ca_cert},
        ),
    )

    client.CoreV1Api().create_namespaced_secret(
        namespace,
        client.V1Secret(
            metadata=client.V1ObjectMeta(
                name=client_secret.metadata.name, labels=client_secret.metadata.labels
            ),
            data={"tls.crt": client_cert, "tls.key": client_key},
        ),
    )
