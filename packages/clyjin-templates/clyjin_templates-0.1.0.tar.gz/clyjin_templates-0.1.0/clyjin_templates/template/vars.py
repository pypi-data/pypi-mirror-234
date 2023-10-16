from enum import Enum

from clyjin.base import Model
from pydantic import RootModel


class TemplateGroupVarSpecialScope(Enum):
    """
    Special keywords for var scopes.

    Attributes:
        All:
            All templates will have this var context.
    """
    All = "$all"


TemplateGroupVarValue = str | int | float | bool
TemplateGroupCustomScope = str
TemplateGroupVarScope = \
    TemplateGroupVarSpecialScope | TemplateGroupCustomScope


class TemplateGroupVar(Model):
    """
    Variable in the template's context.

    Attributes:
        default(optional):
            Default value set to a variable if no value is given on input.
            Defaults to required value, i.e. it will be mandatory to define
            the variable on input.
        scope(optional):
            Scope of a variable.
    """
    default: TemplateGroupVarValue | None = None
    scopes: list[TemplateGroupVarScope] | None = None


class TemplateGroupVarInternal(Model):
    default: TemplateGroupVarValue | None = None
    scopes: list[TemplateGroupVarScope] | None = None
    value: TemplateGroupVarValue
    """
    Final value set for this var at runtime.
    """


class TemplateGroupVars(RootModel):
    root: dict[str, TemplateGroupVar | None]


class TemplateGroupVarsInternal(RootModel):
    # internal variant have var value strictly defined since updating it via
    # different sources
    root: dict[str, TemplateGroupVarInternal]
