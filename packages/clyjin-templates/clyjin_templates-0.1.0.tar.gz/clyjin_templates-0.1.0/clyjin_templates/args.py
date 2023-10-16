from pathlib import Path

from clyjin.base.moduleargs import ModuleArg, ModuleArgs


class TemplatesArgs(ModuleArgs):
    template_group: ModuleArg[str]
    vars: ModuleArg[str]
    target_dir: ModuleArg[Path]


class AddArgs(ModuleArgs):
    template_group_dir: ModuleArg[Path]
    is_update: ModuleArg[bool]
