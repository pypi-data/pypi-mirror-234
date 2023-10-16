from clyjin.base import Model

from clyjin_templates.template.source import TemplateSource
from clyjin_templates.template.vars import (
    TemplateGroupVarScope,
)


class Template(Model):
    """
    Basic unit to be parsed.

    Attributes:
        source(optional):
            Source to fetch a template. Defaults to path to template file
            in the directory of the group spec. The file should have extension
            `.mako` and the same name as provided as a template name in the
            spec.
        scope(optional):
            Variable scope this template works in. Defaults to `$all`.
    """
    source: TemplateSource | None = None
    scopes: list[TemplateGroupVarScope] | None = None
