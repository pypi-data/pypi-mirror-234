import http
import json

import pytest

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.exception import ApiException


def test_update_internal_dai_versions(internal_dai_version_client, internal_dai_versions_cleanup_after):
    v = internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.6-update",
        image="dai-1.10.6-update",
        image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_ALWAYS,
        image_pull_secrets=["secret1", "secret2"],
        aliases=["some-alias"],
        gpu_resource_name="amd.com/gpu",
        data_directory_storage_class="whatever storage class",
        annotations={"key1": "value1", "key2": "value2"}
    )

    v.version = "will be ignored"
    v.image = "dai-1.10.6-update-new-image"
    v.image_pull_policy = ImagePullPolicy.IMAGE_PULL_POLICY_NEVER
    v.image_pull_secrets = ["secret1", "secret3"]
    v.aliases = ["some-alias", "one-more-alias"]
    v.gpu_resource_name = "nvidia.com/gpu"
    v.data_directory_storage_class = "another storage class"
    v.annotations = {"key1": "value1-updated", "key2": "value2", "key3": "value3"}

    updated = internal_dai_version_client.update_version(internal_dai_version=v)

    assert updated.name == "internalDAIVersions/1.10.6-update"
    assert updated.version == "1.10.6-update"
    assert updated.image == "dai-1.10.6-update-new-image"
    assert updated.image_pull_policy == ImagePullPolicy.IMAGE_PULL_POLICY_NEVER
    assert updated.image_pull_secrets == ["secret1", "secret3"]
    assert updated.aliases == ["some-alias", "one-more-alias"]
    assert updated.gpu_resource_name == "nvidia.com/gpu"
    assert updated.data_directory_storage_class == "another storage class"
    assert updated.annotations == {"key1": "value1-updated", "key2": "value2", "key3": "value3"}


def test_update_alias_conflict(internal_dai_version_client, internal_dai_versions_cleanup_after):
    internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.6-update-same-alias",
        image="whatever",
        aliases=["alias-1"],
    )

    v2 = internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.7-update-same-alias",
        image="whatever",
        aliases=["alias-2"],
    )

    v2.aliases = ["alias-1", "alias-2"]

    with pytest.raises(ApiException) as exc:
        internal_dai_version_client.update_version(internal_dai_version=v2)
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST
    assert 'validation error: version 1.10.6-update-same-alias has alias alias-1, ' \
           'cannot have another version with alias alias-1' == json.loads(exc.value.body)["message"]
