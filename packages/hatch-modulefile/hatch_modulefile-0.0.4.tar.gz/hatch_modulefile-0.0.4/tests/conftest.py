import errno
import os
import shutil
import sys
from pathlib import Path
from stat import S_IRWXG, S_IRWXO, S_IRWXU
from tempfile import TemporaryDirectory
from typing import Generator

import pytest


def handle_remove_readonly(func, path, exc):  # no cov
    if func in (os.rmdir, os.remove, os.unlink) and exc[1].errno == errno.EACCES:
        os.chmod(path, S_IRWXU | S_IRWXG | S_IRWXO)
        func(path)
    else:
        raise


@pytest.fixture(scope="session")
def plugin_dir() -> Generator[Path, None, None]:
    with TemporaryDirectory() as d:
        directory = Path(d, "plugin")
        shutil.copytree(Path.cwd(), directory)

        yield directory.resolve()

        shutil.rmtree(directory, ignore_errors=False, onerror=handle_remove_readonly)


@pytest.fixture
def new_project(plugin_dir: Path, tmp_path: Path) -> Generator[Path, None, None]:
    project_dir = tmp_path / "my-app"
    project_dir.mkdir()

    project_file = project_dir / "pyproject.toml"
    project_file.write_text(
        f"""\
[build-system]
requires = ["hatchling", "hatch-modulefile @ {plugin_dir.as_uri()}"]
build-backend = "hatchling.build"

[project]
name = "my-app"
dynamic = ["version"]
requires-python = ">={sys.version_info[0]}"

[tool.hatch.version]
path = "my_app/__init__.py"

[tool.hatch.build.hooks.modulefile]
requires = [
    "python/3.7",
    "my_module"
]
extra-paths = [
    {{type="setenv", variable="QT_XCB_GL_INTEGRATION", value="none"}},
    {{type="prepend-path", variable="PATH", value="/my/custom/path"}},
    {{type="append-path", variable="OTHER_VARIABLE", value="/my/custom/path2"}}
]
""",
        encoding="utf-8",
    )

    package_dir = project_dir / "my_app"
    package_dir.mkdir()

    package_root = package_dir / "__init__.py"
    package_root.write_text('__version__ = "1.2.3"', encoding="utf-8")

    origin = os.getcwd()
    os.chdir(project_dir)
    try:
        yield project_dir
    finally:
        os.chdir(origin)
