import pytest

from clyjin_templates.conversion import FileNodeConversionUtils
from clyjin_templates.filesystem.models import (
    FileNode,
    FileNodeInternal,
)
from clyjin_templates.template.group import TemplateGroup


@pytest.fixture
def s1_root_node(s1_templategroup: TemplateGroup) -> FileNode:
    return s1_templategroup.tree


@pytest.fixture
def s1_root_node_internal(s1_root_node: FileNode) -> FileNodeInternal:
    return FileNodeConversionUtils.convert_to_internal(s1_root_node)
