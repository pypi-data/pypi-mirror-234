import http

import pytest

from h2o_engine_manager.clients.exception import ApiException
from h2o_engine_manager.clients.h2o_version.h2o_version import H2OVersion


def test_list_all_h2o_version(h2o_engine_client):
    expected = [
        H2OVersion(version="3.40.0.3", aliases=["smoker"], deprecated=False, annotations={}),
        H2OVersion(version="3.38.0.4", aliases=[], deprecated=False, annotations={}),
        H2OVersion(version="3.36.1.5", aliases=[], deprecated=False, annotations={"bar": "baz"}),
        H2OVersion(version="0.0.0.0", aliases=["mock"], deprecated=False, annotations={}),
        H2OVersion(version="0.0.0.0-latest", aliases=["latest"], deprecated=False, annotations={}),
    ]

    # When
    h2o_versions = h2o_engine_client.list_all_versions()

    # Then
    for i in range(0, len(expected)):
        assert expected[i].__dict__ == h2o_versions[i].__dict__


def test_paging_h2o_versions(h2o_engine_client):
    # When - list first page.
    first_page = h2o_engine_client.list_versions(page_size=1)

    # Then
    assert first_page.total_size == 5
    assert len(first_page.h2o_versions) == 1
    assert first_page.next_page_token != ""

    # When - list second (last) page.
    second_page = h2o_engine_client.list_versions(
        page_size=5, page_token=first_page.next_page_token
    )

    # Then
    assert second_page.total_size == 5
    assert len(second_page.h2o_versions) == 4
    assert second_page.next_page_token == ""
    assert first_page.h2o_versions[0].version != second_page.h2o_versions[0].version


def test_incorrect_page_token(h2o_engine_client):
    with pytest.raises(ApiException) as exc:
        h2o_engine_client.list_versions(page_token="non-existing-token")
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("order_by", ["non-supported-field", "version unknown-order"])
def test_incorrect_order_by(h2o_engine_client, order_by):
    with pytest.raises(ApiException) as exc:
        h2o_engine_client.list_versions(order_by=order_by)
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


def test_page_size(h2o_engine_client):
    # When - request page size greater than total number of items.
    page = h2o_engine_client.list_versions(page_size=10000)

    # Then
    assert page.total_size == 5


def test_filter(h2o_engine_client):
    # When supported filter expression (alias values are supported).
    vs = h2o_engine_client.list_versions(
        filter="version < \"smoker\" AND version >= \"3.38.0.0\""
    )

    # Then only one H2OVersion conforms to the filter expression
    assert vs.total_size == 1
    assert vs.next_page_token == ""
    assert len(vs.h2o_versions) == 1
    assert vs.h2o_versions[0].version == "3.38.0.4"


def test_invalid_filter_expr(h2o_engine_client):
    with pytest.raises(ApiException) as exc:
        # alias field is not supported for filtering
        h2o_engine_client.list_versions(filter="alias = latest")
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST
