import os

from kubernetes import config

from testing.kubectl import kubectl_apply_dir

config.load_config()
system_namespace = os.getenv("TEST_K8S_SYSTEM_NAMESPACE")

# Create DAISetups.
kubectl_apply_dir(
    dir_path=(os.path.join(os.path.dirname(__file__), "test_data", "dai_setups")),
    namespace=system_namespace,
)

