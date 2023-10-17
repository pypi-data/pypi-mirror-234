import time

from tests.integration.conftest import CACHE_SYNC_SECONDS


def test_list_all_internal_dai_versions(internal_dai_version_client, internal_dai_versions_cleanup_after):
    internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.4",
        image="dai-1.10.4"
    )
    internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.5",
        image="dai-1.10.5"
    )
    internal_dai_version_client.create_version(
        internal_dai_version_id="1.10.6",
        image="dai-1.10.6",
        aliases=["latest"],
    )

    time.sleep(CACHE_SYNC_SECONDS)

    versions = internal_dai_version_client.list_all_versions()

    assert len(versions) == 3

    assert versions[0].version == "1.10.6"
    assert versions[0].image == "dai-1.10.6"
    assert len(versions[0].aliases) == 1
    assert versions[0].aliases[0] == "latest"

    assert versions[1].version == "1.10.5"
    assert versions[1].image == "dai-1.10.5"
    assert len(versions[1].aliases) == 0

    assert versions[2].version == "1.10.4"
    assert versions[2].image == "dai-1.10.4"
    assert len(versions[2].aliases) == 0
