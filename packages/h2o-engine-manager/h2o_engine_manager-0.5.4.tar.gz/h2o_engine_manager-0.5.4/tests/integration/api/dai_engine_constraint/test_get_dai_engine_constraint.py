def test_default_constraint_set(dai_engine_constraint_set_client):
    # Given (global setup):
    # "system.default" DriverlessAISetup exists
    # "definitely-not-existing-workspace-dai-engine-constraint-set" DriverlessAISetup does not exist

    # When getting daiEngineConstraintSet from workspace without DriverlessAISetup
    constraint_set = dai_engine_constraint_set_client.get_constraint_set(
        workspace_id="definitely-not-existing-workspace-dai-engine-constraint-set"
    )

    # Then daiEngineConstraintSet should be equal to default (system.default DriverlessAISetup)
    assert constraint_set.cpu.min == "1"
    assert constraint_set.cpu.max is None
    assert constraint_set.cpu.default == "1"

    assert constraint_set.gpu.min == "0"
    assert constraint_set.gpu.max is None
    assert constraint_set.gpu.default == "0"

    assert constraint_set.memory_bytes.min == "1073741824"
    assert constraint_set.memory_bytes.max == "1099511627776"
    assert constraint_set.memory_bytes.default == "1073741824"

    assert constraint_set.storage_bytes.min == "1073741824"
    assert constraint_set.storage_bytes.max == "1099511627776"
    assert constraint_set.storage_bytes.default == "1073741824"

    assert constraint_set.max_idle_duration.min == "300s"
    assert constraint_set.max_idle_duration.max == "720000s"
    assert constraint_set.max_idle_duration.default == "14400s"

    assert constraint_set.max_running_duration.min == "300s"
    assert constraint_set.max_running_duration.max == "720000s"
    assert constraint_set.max_running_duration.default == "14400s"


def test_workspace_constraint_set(dai_engine_constraint_set_client):
    # Given (global setup):
    # "system.default" DriverlessAISetup exists
    # "existing-dai-engine-constraint-set" DriverlessAISetup does exist

    # When getting daiEngineConstraintSet from workspace without DriverlessAISetup
    constraint_set = dai_engine_constraint_set_client.get_constraint_set(
        workspace_id="existing-dai-engine-constraint-set"
    )

    # Then daiEngineConstraintSet should be equal to existing-dai-engine-constraint-set setup
    assert constraint_set.cpu.min == "1"
    assert constraint_set.cpu.max == "20"
    assert constraint_set.cpu.default == "1"

    assert constraint_set.gpu.min == "0"
    assert constraint_set.gpu.max == "30"
    assert constraint_set.gpu.default == "0"

    assert constraint_set.memory_bytes.min == "1073741824"
    assert constraint_set.memory_bytes.max is None
    assert constraint_set.memory_bytes.default == "1073741824"

    assert constraint_set.storage_bytes.min == "1073741824"
    assert constraint_set.storage_bytes.max is None
    assert constraint_set.storage_bytes.default == "1073741824"

    assert constraint_set.max_idle_duration.min == "600s"
    assert constraint_set.max_idle_duration.max is None
    assert constraint_set.max_idle_duration.default == "7200s"

    assert constraint_set.max_running_duration.min == "600s"
    assert constraint_set.max_running_duration.max is None
    assert constraint_set.max_running_duration.default == "7200s"
