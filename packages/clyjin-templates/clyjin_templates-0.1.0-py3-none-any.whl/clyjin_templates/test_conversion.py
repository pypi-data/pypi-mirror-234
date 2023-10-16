from clyjin_templates.conversion import TemplateGroupConversionUtils
from clyjin_templates.filesystem.models import (
    FileNodeInternal,
    NodeType,
)
from clyjin_templates.template.group import (
    TemplateGroup,
    TemplateGroupInternal,
)
from clyjin_templates.template.vars import (
    TemplateGroupVarInternal,
    TemplateGroupVarsInternal,
)


def test_convert():
    group: TemplateGroup = TemplateGroup.model_validate({
        "name": "test",
        "tree": {
            "main.py": {
                "$content": "print(${a})",
            },
            "service.py": {
                "$content": "&service.py",
            },
            "readme": {
                "$content": "hello!",
            },
        },
        "templates": {
            "service.py": None,
        },
        "description": "Test template!",
        "vars": {
            "a": {
                "default": 1,
            },
        },
    })

    internal: TemplateGroupInternal = \
        TemplateGroupConversionUtils.convert_to_internal(
            group,
            {
                "a": 5,
            },
        )

    expected: TemplateGroupInternal = TemplateGroupInternal(
        name="test",
        tree=FileNodeInternal(
            type=NodeType.Dir,
            nodes={
                "main.py": FileNodeInternal(
                    type=NodeType.File,
                    content="print(${a})",
                ),
                "service.py": FileNodeInternal(
                    type=NodeType.File,
                    content="&service.py",
                ),
                "readme": FileNodeInternal(
                    type=NodeType.File,
                    content="hello!",
                ),
            },
        ),
        templates={
            "service.py": None,
        },
        description="Test template!",
        vars=TemplateGroupVarsInternal(
            root={
                "a": TemplateGroupVarInternal(
                    default=1,
                    value=5,
                ),
            },
        ),
    )

    assert internal == expected
