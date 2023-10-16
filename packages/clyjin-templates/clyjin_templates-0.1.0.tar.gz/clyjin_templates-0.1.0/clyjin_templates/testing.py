from pathlib import Path

import pytest


@pytest.fixture
def tests_dir() -> Path:
    return Path("tests")


@pytest.fixture
def tests_template_groups_dir(tests_dir: Path) -> Path:
    return Path(tests_dir, "templategroups")


@pytest.fixture
def s1_templategroup_dir(tests_template_groups_dir: Path) -> Path:
    return Path(
        tests_template_groups_dir,
        "s1",
    )
