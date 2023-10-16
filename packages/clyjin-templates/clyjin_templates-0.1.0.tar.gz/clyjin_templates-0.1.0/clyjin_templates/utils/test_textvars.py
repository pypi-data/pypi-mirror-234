import pytest

from clyjin_templates.utils.textvars import TextVarsMap, TextVarsUtils


@pytest.mark.parametrize(
    "text,expected",
    [
        (
            "a=2,bo=2.1,co='hello, world!',d=true,e='true',f='wow=!'",
            {
                "a": 2,
                "bo": 2.1,
                "co": "hello, world!",
                "d": True,
                "e": "true",
                "f": "wow=!",
            },
        ),
    ],
)
def test_convert(text: str, expected: TextVarsMap | type[Exception]):
    if isinstance(expected, dict):
        assert TextVarsUtils.convert(text) == expected
        return

    try:
        TextVarsUtils.convert(text)
    except expected:
        return
    else:
        raise AssertionError
