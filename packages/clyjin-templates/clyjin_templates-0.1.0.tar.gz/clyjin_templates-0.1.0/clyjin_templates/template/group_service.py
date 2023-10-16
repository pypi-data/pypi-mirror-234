import asyncio
import os
import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Coroutine

from antievil import DirectoryExpectError, DuplicateNameError, NotFoundError
from clyjin.log import Log

from clyjin_templates.parsers import TemplateGroupSpecParser
from clyjin_templates.template.errors import IncorrectTemplateGroupNameError
from clyjin_templates.utils.service import Service
from clyjin_templates.utils.yml import load_yml

if TYPE_CHECKING:
    from clyjin_templates.template.group import TemplateGroup


class TemplateGroupService(Service):
    """
    Manages Template Groups.
    """
    def __init__(
        self,
        root_dir: Path,
        groups_dir: Path,
    ) -> None:
        self._root_dir: Path = root_dir
        self._groups_dir: Path = groups_dir
        self._is_loaded: bool = False
        self._group_by_name: dict[str, "TemplateGroup"] = {}

    @property
    def groups_dir(self) -> Path:
        return self._groups_dir

    def get(self, name: str) -> "TemplateGroup":
        """
        Gets group by name.
        """
        try:
            return self._group_by_name[name]
        except KeyError as error:
            raise NotFoundError(
                title="template group with name",
                value=name,
            ) from error

    async def add(
        self,
        dir: Path,
        *,
        is_update: bool = False,
    ) -> str:
        """
        Adds a new template group to the storage.

        The name for a new template group will be fetched from the spec.yml
        file and returned on successful add.

        Args:
            dir:
                Directory where a template group resides. The dir should
                contain at least `spec.yml` file at the root level.
        """
        self._softcheck_group_dir(dir)
        final_name: str = self._get_group_name(dir)
        self._check_name_correctness(final_name)
        if not is_update:
            self._check_name_existence(final_name)

        Log.info(
            f"[clyjin_templates] adding template <{final_name}>"
            f" group from path <{dir}>",
        )

        destination_dir: Path = Path(
            self._groups_dir,
            final_name,
        )

        Log.info(
            f"[clyjin_templates] copying group <{final_name}>"
            f" from <{dir}> to <{destination_dir}>",
        )

        # TODO(ryzhovalex): copy only required stuff, i.e. mako and spec.yml
        shutil.copytree(
            dir,
            destination_dir,
            dirs_exist_ok=is_update,
        )

        # TODO(ryzhovalex): why do i need load here?
        await self._load(final_name)

        return final_name

    def _get_group_name(self, spec_dir: Path) -> str:
        return load_yml(Path(
            spec_dir,
            "spec.yml",
        ))["name"]

    async def preload(self) -> None:
        """
        Loads saved groups into memory.
        """
        loading_coros: list[Coroutine[None, None, None]] = []

        for _, dirnames, _ in os.walk(self._groups_dir):
            loading_coros.extend([self._load(dirname) for dirname in dirnames])

        if len(loading_coros) > 0:
            await asyncio.gather(*loading_coros)
        else:
            Log.warning("[clyjin_templates] nothing to preload")

    async def _load(self, name: str) -> None:
        """
        Loads template groups from storage into main memory.
        """
        group_dir: Path = Path(
            self._groups_dir,
            name,
        )
        self._softcheck_group_dir(group_dir)

        spec_path: Path = Path(
            group_dir,
            "spec.yml",
        )
        self._group_by_name[name] = TemplateGroupSpecParser().parse(spec_path)

    def _check_name_correctness(self, name: str) -> None:
        """
        Checks group name for correctness.
        """
        if name == "":
            raise IncorrectTemplateGroupNameError(name, "empty")
        elif not name.isalnum():
            raise IncorrectTemplateGroupNameError(name, "not alpha-numeric")

    def _check_name_existence(self, name: str) -> None:
        """
        Checks group name for existence in storage.
        """
        if name in self._group_by_name:
            raise DuplicateNameError(
                title="template group name",
                name=name,
            )

    def _softcheck_group_dir(self, group_dir: Path) -> None:
        """
        Checks that a group dir should contain at least `spec.yml` file.

        Other checks, such as proper structure of `spec.yml` will be done only
        at the first template call.

        Maybe in future the initial check will be performed outputting the
        template to some temporary directory for test purposes.
        """
        if not group_dir.is_dir():
            raise DirectoryExpectError(path=group_dir)
        elif not Path(group_dir, "spec.yml").is_file():
            raise NotFoundError(
                title="spec file for template group dir",
                value=group_dir,
            )
