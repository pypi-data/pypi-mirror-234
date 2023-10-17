import os

from kubernetes import config

from testing.kubectl import create_dai_license
from testing.kubectl import kubectl_apply_dir
from testing.kubectl import setup_mlops_secrets

config.load_config()
system_namespace = os.getenv("TEST_K8S_SYSTEM_NAMESPACE")

# Not checking DAIVersions because we are creating unsupported version 1.10.3
# (so we're ignoring webhook)
kubectl_apply_dir(
    dir_path=(os.path.join(os.path.dirname(__file__), "test_data", "dai_versions")),
    namespace=system_namespace,
    check=False,
)
kubectl_apply_dir(
    dir_path=(os.path.join(os.path.dirname(__file__), "test_data", "h2o_versions")),
    namespace=system_namespace,
)
kubectl_apply_dir(
    dir_path=(os.path.join(os.path.dirname(__file__), "test_data", "dai_setups")),
    namespace=system_namespace,
)
kubectl_apply_dir(
    dir_path=(os.path.join(os.path.dirname(__file__), "test_data", "h2o_setups")),
    namespace=system_namespace,
)

create_dai_license(namespace=system_namespace)

if os.getenv("MLOPS_CLUSTER") == "true":
    setup_mlops_secrets(namespace=system_namespace)
