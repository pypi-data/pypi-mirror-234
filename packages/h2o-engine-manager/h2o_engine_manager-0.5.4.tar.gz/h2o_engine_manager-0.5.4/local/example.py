import os

import h2o_engine_manager

workspace_id = "my-workspace"
engine_id = "my-engine"

daiengine_client = h2o_engine_manager.login_custom(
    endpoint="http://localhost:8080",
    refresh_token=os.getenv("PLATFORM_TOKEN_USER"),
    client_id="hac-platform-public",
    issuer_url="https://auth.cloud-dev.h2o.ai/auth/realms/hac-dev",
).dai_engine_client

print(f"total engines ({workspace_id}): {daiengine_client.list_engines(workspace_id=workspace_id).total_size}")

engine = daiengine_client.create_engine(
    workspace_id=workspace_id,
    engine_id=engine_id,
    version="1.10.4",
    cpu=1,
    gpu=0,
    memory_bytes="8Gi",
    storage_bytes="16Gi",
    max_idle_duration="15m",
    max_running_duration="2d",
    display_name="My engine",
)
print(f"{engine_id}: {engine.state.value}")

engine.wait()

print(f"{engine_id}: {engine.state.value}")
print(f"total engines ({workspace_id}): {daiengine_client.list_engines(workspace_id=workspace_id).total_size}")

engine.connect()

engine.delete()
print(f"{engine_id}: {engine.state.value}")

engine.wait(timeout_seconds=100)
print(f"total engines ({workspace_id}): {daiengine_client.list_engines(workspace_id=workspace_id).total_size}")
