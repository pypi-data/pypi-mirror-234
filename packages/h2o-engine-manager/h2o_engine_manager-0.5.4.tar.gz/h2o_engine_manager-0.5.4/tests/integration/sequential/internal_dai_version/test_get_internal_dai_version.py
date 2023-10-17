import time

from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_get_internal_dai_version(internal_dai_version_client, internal_dai_versions_cleanup_after):
    internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.6-get",
        image="1.10.6-get",
        aliases=["some-alias"]
    )

    # Wait to make sure the created dai version is synced in cache.
    time.sleep(CACHE_SYNC_SECONDS)

    v = internal_dai_version_client.get_version(internal_dai_version_id="1.10.6-get")

    assert v.name == "internalDAIVersions/1.10.6-get"
    assert v.version == "1.10.6-get"
    assert v.internal_dai_version_id == "1.10.6-get"

    # Test getting by alias
    v_alias = internal_dai_version_client.get_version(internal_dai_version_id="some-alias")

    # Need to compare field by field (v and v_alias are different objects but with same values)
    assert v.name == v_alias.name
    assert v.internal_dai_version_id == v_alias.internal_dai_version_id
    assert v.version == v_alias.version
    assert v.image == v_alias.image
    assert v.image_pull_policy == v_alias.image_pull_policy
    assert v.image_pull_secrets == v_alias.image_pull_secrets
    assert v.aliases == v_alias.aliases
    assert v.data_directory_storage_class == v_alias.data_directory_storage_class
    assert v.gpu_resource_name == v_alias.gpu_resource_name
    assert v.deprecated == v_alias.deprecated
    assert v.annotations == v_alias.annotations
