from clyjin.base import Model

from clyjin_templates.filesystem.models import FileNode, FileNodeInternal
from clyjin_templates.template.template import Template
from clyjin_templates.template.vars import (
    TemplateGroupVars,
    TemplateGroupVarsInternal,
)


class TemplateGroup(Model):
    """
    Collection of templates executed at once to form a directory structure.

    Attributes:
        name:
            Name of a group.
        tree:
            File tree structure for a group.
        templates(optional):
            Templates attached to a group. Named without `.mako` suffix.
            Defaults to None.
        description(optional):
            Description text of a group. Defaults to None.
        vars(optional):
            Variables context of this group. Defaults to None.
    """
    name: str
    tree: FileNode
    templates: dict[str, Template | None] | None = None
    description: str | None = None
    vars: TemplateGroupVars | None = None


class TemplateGroupInternal(Model):
    name: str
    tree: FileNodeInternal
    templates: dict[str, Template | None] | None = None
    description: str | None = None
    vars: TemplateGroupVarsInternal | None = None
