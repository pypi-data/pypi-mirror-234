import http

import pytest

from h2o_engine_manager.clients.dai_version.dai_version import DAIVersion
from h2o_engine_manager.clients.exception import ApiException


def test_list_all_dai_version(dai_client):
    # Arrange - DAIVersion CRDs are already present in the cluster.
    expected = [
        DAIVersion(version="1.10.6.1", aliases=["latest"], deprecated=False, annotations={}),
        DAIVersion(version="1.10.6.1-alpha", aliases=[], deprecated=False, annotations={}),
        DAIVersion(version="1.10.6", aliases=[], deprecated=False, annotations={}),
        DAIVersion(version="1.10.5", aliases=[], deprecated=False, annotations={}),
        DAIVersion(version="1.10.5-mock", aliases=["mock", "alias-foo"], deprecated=False, annotations={}),
        DAIVersion(version="1.10.5-do-not-use-me", aliases=[], deprecated=False, annotations={}),
        DAIVersion(version="1.10.4", aliases=[], deprecated=False, annotations={"foo": "foo"}),
        DAIVersion(version="1.10.3", aliases=[], deprecated=True, annotations={}),
    ]

    # When
    dai_versions = dai_client.list_all_versions()

    # Then
    for i in range(0, len(expected)):
        assert expected[i].__dict__ == dai_versions[i].__dict__


def test_paging_dai_versions(dai_client):
    # Arrange - DAIVersion CRDs are already present in the cluster.

    # When - list first page.
    first_page = dai_client.list_versions(page_size=1)

    # Then
    assert first_page.total_size == 8
    assert len(first_page.dai_versions) == 1
    assert first_page.next_page_token != ""

    # When - list second (last) page.
    second_page = dai_client.list_versions(
        page_size=7, page_token=first_page.next_page_token
    )

    # Then
    assert second_page.total_size == 8
    assert len(second_page.dai_versions) == 7
    assert second_page.next_page_token == ""
    assert first_page.dai_versions[0].version != second_page.dai_versions[0].version


def test_incorrect_page_token(dai_client):
    with pytest.raises(ApiException) as exc:
        dai_client.list_versions(page_token="non-existing-token")
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize("order_by", ["non-supported-field", "version unknown-order"])
def test_incorrect_order_by(dai_client, order_by):
    with pytest.raises(ApiException) as exc:
        dai_client.list_versions(order_by=order_by)
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST


def test_page_size(dai_client):
    # When - request page size greater than total number of items.
    page = dai_client.list_versions(page_size=10000)

    # Then
    assert page.total_size == 8


def test_filter(dai_client):
    # When supported filter expression (alias values are supported).
    vs = dai_client.list_versions(filter="version < \"latest\" AND version > \"1.10.6\"")

    # Then only one DAIVersion conforms to the filter expression
    assert vs.total_size == 1
    assert vs.next_page_token == ""
    assert len(vs.dai_versions) == 1
    assert vs.dai_versions[0].version == "1.10.6.1-alpha"


def test_invalid_filter_expr(dai_client):
    with pytest.raises(ApiException) as exc:
        # alias field is not supported for filtering
        dai_client.list_versions(filter="alias = latest")
    assert exc.value.status == http.HTTPStatus.BAD_REQUEST
