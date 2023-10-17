def test_get_default_constraint_set(h2o_engine_constraint_set_client):
    # Given (global setup):
    # "system.default" H2OSetup exists
    # "definitely-not-existing-workspace-h2o-engine-constraint-set" H2OSetup does not exist

    # When getting h2oEngineConstraintSet from workspace without DriverlessAISetup
    constraint_set = h2o_engine_constraint_set_client.get_constraint_set(
        workspace_id="definitely-not-existing-workspace-h2o-engine-constraint-set"
    )

    # Then h2oEngineConstraintSet should be equal to default (system.default H2OSetup)
    assert constraint_set.node_count.min == "1"
    assert constraint_set.node_count.max is None
    assert constraint_set.node_count.default == "1"

    assert constraint_set.cpu.min == "1"
    assert constraint_set.cpu.max is None
    assert constraint_set.cpu.default == "1"

    assert constraint_set.gpu.min == "0"
    assert constraint_set.gpu.max is None
    assert constraint_set.gpu.default == "0"

    assert constraint_set.memory_bytes.min == "2147483648"
    assert constraint_set.memory_bytes.max is None
    assert constraint_set.memory_bytes.default == "4294967296"

    assert constraint_set.max_idle_duration.min == "0s"
    assert constraint_set.max_idle_duration.max is None
    assert constraint_set.max_idle_duration.default == "3600s"

    assert constraint_set.max_running_duration.min == "0s"
    assert constraint_set.max_running_duration.max is None
    assert constraint_set.max_running_duration.default == "14400s"


def test_get_workspace_constraint_set(h2o_engine_constraint_set_client):
    # Given (global setup):
    # "system.default" H2OSetup exists
    # "existing-h2o-engine-constraint-set" H2OSetup does exist

    # When getting h2oEngineConstraintSet from workspace without H2OSetup
    constraint_set = h2o_engine_constraint_set_client.get_constraint_set(
        workspace_id="existing-h2o-engine-constraint-set"
    )

    # Then h2oEngineConstraintSet should be equal to existing-h2o-engine-constraint-set
    assert constraint_set.node_count.min == "1"
    assert constraint_set.node_count.max == "10"
    assert constraint_set.node_count.default == "3"

    assert constraint_set.cpu.min == "2"
    assert constraint_set.cpu.max == "4"
    assert constraint_set.cpu.default == "2"

    assert constraint_set.gpu.min == "1"
    assert constraint_set.gpu.max is None
    assert constraint_set.gpu.default == "1"

    assert constraint_set.memory_bytes.min == "2147483648"
    assert constraint_set.memory_bytes.max is None
    assert constraint_set.memory_bytes.default == "4294967296"

    assert constraint_set.max_idle_duration.min == "0s"
    assert constraint_set.max_idle_duration.max is None
    assert constraint_set.max_idle_duration.default == "3600s"

    assert constraint_set.max_running_duration.min == "0s"
    assert constraint_set.max_running_duration.max is None
    assert constraint_set.max_running_duration.default == "14400s"
