import http

import pytest

from h2o_engine_manager.clients.exception import ApiException


def test_create_unauthorized(
    internal_h2o_version_client_admin,
    internal_h2o_versions_cleanup_after,
):
    with pytest.raises(ApiException) as exc:
        internal_h2o_version_client_admin.create_version(
            internal_h2o_version_id="3.40.0.3-create-unauthorized",
            image="whatever",
        )
    assert exc.value.status == http.HTTPStatus.FORBIDDEN


def test_get_unauthorized(
    internal_h2o_version_client_standard_user,
    internal_h2o_version_client,
    internal_h2o_versions_cleanup_after
):
    internal_h2o_version_client.create_version(
        internal_h2o_version_id="3.40.0.3-get-unauthorized",
        image="whatever"
    )

    with pytest.raises(ApiException) as exc:
        internal_h2o_version_client_standard_user.get_version(
            internal_h2o_version_id="3.40.0.3-get-unauthorized"
        )
    assert exc.value.status == http.HTTPStatus.FORBIDDEN


def test_list_unauthorized(internal_h2o_version_client_admin):
    with pytest.raises(ApiException) as exc:
        internal_h2o_version_client_admin.list_versions()
    assert exc.value.status == http.HTTPStatus.FORBIDDEN


def test_update_unauthorized(
    internal_h2o_version_client_standard_user,
    internal_h2o_version_client,
    internal_h2o_versions_cleanup_after
):
    v = internal_h2o_version_client.create_version(
        internal_h2o_version_id="3.40.0.3-update-unauthorized",
        image="whatever"
    )
    v.gpu_resource_name = "foo"

    with pytest.raises(ApiException) as exc:
        internal_h2o_version_client_standard_user.update_version(internal_h2o_version=v)
    assert exc.value.status == http.HTTPStatus.FORBIDDEN


def test_delete_unauthorized(
    internal_h2o_version_client_standard_user,
    internal_h2o_version_client,
    internal_h2o_versions_cleanup_after
):
    internal_h2o_version_client.create_version(
        internal_h2o_version_id="3.40.0.3-delete-unauthorized",
        image="whatever"
    )

    with pytest.raises(ApiException) as exc:
        internal_h2o_version_client_standard_user.delete_version(internal_h2o_version_id="3.40.0.3-delete-unauthorized")
    assert exc.value.status == http.HTTPStatus.FORBIDDEN
