import re

import pytest

from h2o_engine_manager.clients.engine_id.generator import generate_engine_id
from h2o_engine_manager.clients.engine_id.generator import sanitize_display_name
from h2o_engine_manager.gen.dai_engine_service import ApiException


@pytest.mark.parametrize(
    "display_name,expected",
    [
        ("Valid Name", "valid-name"),
        ("133t", "t"),
        ("  what spaces?   ", "what-spaces"),
        ("", ""),
        ("_underscore", "underscore"),
        ("-dash-", "dash"),
        ("----", ""),
        ("Some very long but very useful display name for my most beloved artificial intelligence engine.", "some-very-long-but-very-useful-display-name-for-my-most-be"),
    ],
)
def test_sanitize_display_name(display_name, expected):
    assert sanitize_display_name(display_name=display_name) == expected


class MockEngineGetter:
    def __init__(self):
        self.called = False

    def get_engine(self, engine_id: str, workspace_id: str):
        # If a specific engine has been requested before, return no exception = engine found.
        if engine_id == "a" and self.called:
            return

        self.called = True
        raise ApiException(status=404, reason="Engine not found")


@pytest.mark.parametrize(
    "display_name,expected",
    [
        ("unused", "unused"),
        ("", "new-dai-engine"),
    ],
)
def test_generate_engine_id(display_name, expected):
    assert generate_engine_id(display_name=display_name, workspace_id="default", engine_type="dai", engine_getter=MockEngineGetter().get_engine) == expected


def test_generate_engine_rand():
    engine_getter = MockEngineGetter()
    name_1 = generate_engine_id(display_name="a", workspace_id="default", engine_type="dai", engine_getter=engine_getter.get_engine)
    name_2 = generate_engine_id(display_name="a", workspace_id="default", engine_type="dai", engine_getter=engine_getter.get_engine)
    name_3 = generate_engine_id(display_name="a", workspace_id="default", engine_type="dai", engine_getter=engine_getter.get_engine)

    pattern = re.compile("^a-[0-9]{4}$")
    assert pattern.match(name_2)
    assert pattern.match(name_3)
    assert name_1 != name_2 != name_3
