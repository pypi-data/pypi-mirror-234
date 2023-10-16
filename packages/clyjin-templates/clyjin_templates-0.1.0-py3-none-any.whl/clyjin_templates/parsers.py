from pathlib import Path
from typing import Any

from antievil import FileExpectError

from clyjin_templates.template.group import TemplateGroup
from clyjin_templates.utils.yml import load_yml


class TemplateGroupSpecParser:
    """
    Parses Template Group specification files.
    """
    def parse(
        self,
        spec_path: Path,
    ) -> TemplateGroup:
        self._check_spec_path(spec_path)
        spec: dict[str, Any] = load_yml(spec_path)
        template_group: TemplateGroup = TemplateGroup.model_validate(spec)
        return template_group

    def _check_spec_path(self, path: Path) -> None:
        if not path.is_file():
            raise FileExpectError(path=path)
        elif path.name != "spec.yml":
            # TODO(ryzhovalex): replace with antievil.NameExpectError
            # 0
            raise ValueError
