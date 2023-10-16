from pathlib import Path

import pytest

from clyjin_templates.parsers import TemplateGroupSpecParser
from clyjin_templates.template.group import TemplateGroup


@pytest.fixture
def s1_templategroup(s1_templategroup_dir: Path) -> TemplateGroup:
    return TemplateGroupSpecParser().parse(Path(
        s1_templategroup_dir,
        "spec.yml",
    ))
