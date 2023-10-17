import http
import json

import pytest

from h2o_engine_manager.clients.base.image_pull_policy import ImagePullPolicy
from h2o_engine_manager.clients.exception import ApiException


def test_create(internal_h2o_version_client, internal_h2o_versions_cleanup_after):
    v = internal_h2o_version_client.create_version(
        internal_h2o_version_id="3.40.0.3-create",
        image="whatever",
        image_pull_policy=ImagePullPolicy.IMAGE_PULL_POLICY_ALWAYS,
        image_pull_secrets=["secret1", "secret2"],
        aliases=["some-alias"],
        gpu_resource_name="whatever string because server accepts any value",
        annotations={"key1": "value1", "key2": "value2"}
    )

    assert v.name == "internalH2OVersions/3.40.0.3-create"
    assert v.internal_h2o_version_id == "3.40.0.3-create"
    assert v.version == "3.40.0.3-create"
    assert v.image == "whatever"
    assert v.image_pull_policy == ImagePullPolicy.IMAGE_PULL_POLICY_ALWAYS
    assert v.image_pull_secrets == ["secret1", "secret2"]
    assert v.aliases == ["some-alias"]
    assert v.gpu_resource_name == "whatever string because server accepts any value"
    assert v.annotations == {"key1": "value1", "key2": "value2"}


def test_create_default_values(internal_h2o_version_client, internal_h2o_versions_cleanup_after):
    v = internal_h2o_version_client.create_version(
        internal_h2o_version_id="3.40.0.3-create-default",
        image="whatever"
    )

    assert v.name == "internalH2OVersions/3.40.0.3-create-default"
    assert v.internal_h2o_version_id == "3.40.0.3-create-default"
    assert v.version == "3.40.0.3-create-default"
    assert v.image == "whatever"
    assert v.image_pull_policy == ImagePullPolicy.IMAGE_PULL_POLICY_IF_NOT_PRESENT
    assert v.image_pull_secrets == []
    assert v.aliases == []
    assert v.gpu_resource_name == "nvidia.com/gpu"
    assert v.annotations == {}


def test_create_already_exists(internal_h2o_version_client, internal_h2o_versions_cleanup_after):
    internal_h2o_version_client.create_version(
        internal_h2o_version_id="3.40.0.3-already-exists",
        image="3.40.0.3"
    )

    with pytest.raises(ApiException) as exc:
        # Try to create H2OVersion with the same ID.
        internal_h2o_version_client.create_version(
            internal_h2o_version_id="3.40.0.3-already-exists",
            image="3.40.0.3-foo",
        )

    # grpc AlreadyExists == http Conflict 409
    assert exc.value.status == http.HTTPStatus.CONFLICT


def test_create_alias_conflict(internal_h2o_version_client, internal_h2o_versions_cleanup_after):
    internal_h2o_version_client.create_version(
        internal_h2o_version_id="3.40.0.3-create-alias-conflict",
        image="h2o-3.40.0.3",
        aliases=["foo"]
    )

    with pytest.raises(ApiException) as exc:
        # Try to create H2OVersion with an already used alias.
        internal_h2o_version_client.create_version(
            internal_h2o_version_id="3.40.0.4-create-alias-conflict",
            image="h2o-3.40.0.4",
            aliases=["foo"]
        )

    assert exc.value.status == http.HTTPStatus.BAD_REQUEST
    assert 'validation error: unique constraint violation: version 3.40.0.3-create-alias-conflict has alias foo, ' \
           'cannot have another version with alias foo' == json.loads(exc.value.body)["message"]
