import http

import pytest

from h2o_engine_manager.clients.exception import ApiException


def test_create_unauthorized(internal_dai_version_client_standard_user, internal_dai_versions_cleanup_after):
    with pytest.raises(ApiException) as exc:
        internal_dai_version_client_standard_user.create_version(
            internal_dai_version_id="1.10.6-create-unauthorized",
            image="whatever",
        )
    assert exc.value.status == http.HTTPStatus.FORBIDDEN


def test_get_unauthorized(
    internal_dai_version_client_standard_user,
    internal_dai_version_client,
    internal_dai_versions_cleanup_after,
):
    internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.6-get-unauthorized",
        image="whatever"
    )

    with pytest.raises(ApiException) as exc:
        internal_dai_version_client_standard_user.get_version(
            internal_dai_version_id="1.10.6-get-unauthorized"
        )
    assert exc.value.status == http.HTTPStatus.FORBIDDEN


def test_list_unauthorized(internal_dai_version_client_admin):
    with pytest.raises(ApiException) as exc:
        internal_dai_version_client_admin.list_versions()
    assert exc.value.status == http.HTTPStatus.FORBIDDEN


def test_update_unauthorized(
    internal_dai_version_client_admin,
    internal_dai_version_client,
    internal_dai_versions_cleanup_after
):
    v = internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.6-update-unauthorized",
        image="whatever"
    )
    v.gpu_resource_name = "whatever"

    with pytest.raises(ApiException) as exc:
        internal_dai_version_client_admin.update_version(internal_dai_version=v)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN


def test_delete_unauthorized(
    internal_dai_version_client_admin,
    internal_dai_version_client,
    internal_dai_versions_cleanup_after
):
    internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.6-delete-unauthorized",
        image="whatever"
    )

    with pytest.raises(ApiException) as exc:
        internal_dai_version_client_admin.delete_version(internal_dai_version_id="1.10.6-delete-unauthorized")
    assert exc.value.status == http.HTTPStatus.FORBIDDEN
