import re
from contextlib import suppress

from antievil import EmptyInputError, LengthExpectError

from clyjin_templates.utils.klass import Static

TextVarValue = int | float | bool | str
TextVarsMap = dict[str, TextVarValue]

NonEnclosedRegex: str = r"(?=([^']*'[^']*')*[^']*$)"
"""
Matches all characters not enclosed in quotes

Prepend `\\<your-character>` to specify for which unenclosed character to
search.

Ref: https://stackoverflow.com/a/6464500/14748231
"""

class TextVarsUtils(Static):
    """
    Converts text like "a=1,b=true,c='hello'" to map of variables. Really
    simple my dude!

    Supported types of variables are: str, int, float, bool.

    Vars like "a=true", "a=True", "a=false", "a=False" are converted to the
    respective bools.

    Strings are only accepted enclosed with single quotes to avoid
    user input errors. Double quotes are not supported due to current
    regex patterns limitations.

    Variable names should follow the same rules as for Python names, for the
    consistency.
    """
    @staticmethod
    def convert(text: str) -> TextVarsMap:
        if len(text) == 0:
            raise EmptyInputError(title="text")

        mp: TextVarsMap = {}

        separated: list[str] = []
        prev_end_index: int = 0

        # do not count commas enclosed in string var values
        for m in re.finditer(r"\," + NonEnclosedRegex, text):
            separated.append(text[prev_end_index:m.start(0)])
            prev_end_index = m.end(0)
        # and add the last element
        separated.append(text[prev_end_index:])

        for rawvar in separated:
            separated_rawvar: list[str] = []
            prev_end_index = 0

            # do not count equality sign enclosed in string var values
            for m in re.finditer(r"\=" + NonEnclosedRegex, rawvar):
                separated_rawvar.append(rawvar[prev_end_index:m.start(0)])
                prev_end_index = m.end(0)
            # and add the last element
            separated_rawvar.append(rawvar[prev_end_index:])

            if len(separated_rawvar) != 2:  # noqa:PLR2004
                raise LengthExpectError(
                    separated_rawvar,
                    2,
                    len(separated_rawvar),
                )

            mp[separated_rawvar[0]] = TextVarsUtils.convert_only_value(
                separated_rawvar[1],
            )

        return mp

    @staticmethod
    def convert_only_value(vartext: str) -> TextVarValue:
        if len(vartext) == 0:
            raise EmptyInputError(title="vartext")

        if "." in vartext:
            with suppress(ValueError):
                return float(vartext)

        with suppress(ValueError):
            return int(vartext)

        match vartext:
            case "true" | "True":
                return True
            case "false" | "False":
                return True

        # no quotes should present in the final var value
        return vartext.replace("'", "")
