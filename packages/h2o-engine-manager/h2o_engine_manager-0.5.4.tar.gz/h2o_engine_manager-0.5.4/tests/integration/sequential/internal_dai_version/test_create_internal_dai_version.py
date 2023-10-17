import http
import json

import pytest

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.exception import ApiException


def test_create_internal_dai_version(internal_dai_version_client, internal_dai_versions_cleanup_after):
    v = internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.6-create",
        image="dai-1.10.6-create",
        image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_ALWAYS,
        image_pull_secrets=["secret1", "secret2"],
        aliases=["some-alias"],
        gpu_resource_name="whatever string because server accepts any value",
        data_directory_storage_class="again, YOLO string",
        annotations={"key1": "value1", "key2": "value2"}
    )

    assert v.name == "internalDAIVersions/1.10.6-create"
    assert v.internal_dai_version_id == "1.10.6-create"
    assert v.version == "1.10.6-create"
    assert v.image == "dai-1.10.6-create"
    assert v.image_pull_policy == ImagePullPolicy.IMAGE_PULL_POLICY_ALWAYS
    assert v.image_pull_secrets == ["secret1", "secret2"]
    assert v.aliases == ["some-alias"]
    assert v.gpu_resource_name == "whatever string because server accepts any value"
    assert v.data_directory_storage_class == "again, YOLO string"
    assert v.annotations == {"key1": "value1", "key2": "value2"}


def test_create_internal_dai_version_default_values(internal_dai_version_client, internal_dai_versions_cleanup_after):
    v = internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.6-create-default",
        image="dai-1.10.6-create-default"
    )

    assert v.name == "internalDAIVersions/1.10.6-create-default"
    assert v.internal_dai_version_id == "1.10.6-create-default"
    assert v.version == "1.10.6-create-default"
    assert v.image == "dai-1.10.6-create-default"
    assert v.image_pull_policy == ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT
    assert v.image_pull_secrets == []
    assert v.aliases == []
    assert v.gpu_resource_name == "nvidia.com/gpu"
    assert v.data_directory_storage_class == ""
    assert v.annotations == {}


def test_create_internal_dai_version_already_exists(internal_dai_version_client, internal_dai_versions_cleanup_after):
    internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.6-already-exists",
        image="dai-1.10.6"
    )

    with pytest.raises(ApiException) as exc:
        # Try to create DAIVersion with the same ID.
        internal_dai_version_client.create_version(
            internal_dai_version_id="1.10.6-already-exists",
            image="dai-1.10.6-foo",
        )

    # grpc AlreadyExists == http Conflict 409
    assert exc.value.status == http.HTTPStatus.CONFLICT


def test_create_alias_conflict(internal_dai_version_client, internal_dai_versions_cleanup_after):
    internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.6-create-alias-conflict",
        image="dai-1.10.6",
        aliases=["foo"]
    )

    with pytest.raises(ApiException) as exc:
        # Try to create DAIVersion with an already used alias.
        internal_dai_version_client.create_version(
            internal_dai_version_id="1.10.7-create-alias-conflict",
            image="dai-1.10.7",
            aliases=["foo"]
        )

    assert exc.value.status == http.HTTPStatus.BAD_REQUEST
    assert 'validation error: unique constraint violation: version 1.10.6-create-alias-conflict has alias foo, ' \
           'cannot have another version with alias foo' == json.loads(exc.value.body)["message"]


def test_create_minimal_version_validation(internal_dai_version_client, internal_dai_versions_cleanup_after):
    with pytest.raises(ApiException) as exc:
        internal_dai_version_client.create_version(
            internal_dai_version_id="1.10.3",
            image="dai-1.10.3"
        )
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST
    assert 'validation error: invalid version: version 1.10.3 is not supported, minimal supported version is 1.10.4'
