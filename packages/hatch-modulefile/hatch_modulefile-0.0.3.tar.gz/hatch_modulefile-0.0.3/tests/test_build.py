from __future__ import annotations

from pathlib import Path

import pytest

from .utils import build_project, install_project_venv


@pytest.mark.slow
def test_modulefile(new_project: Path):
    build_project()
    install_directory = install_project_venv()

    modulefile = install_directory.joinpath("lib", "python3.7", "site-packages", "modulefiles", "my_app") # TODO: hard coded for python/3.7
    assert modulefile.exists()

    text = modulefile.read_text()

    requirements = [s.strip() for s in text.split("necessary       {\n")[1].split("}", 1)[0].splitlines()]
    assert requirements == ["python/3.7", "my_module"]
    assert get_setting(text, "setenv") == [["PYTHON_ROOT", "$venv"], ["QT_XCB_GL_INTEGRATION", "none"]]
    assert get_setting(text, "prepend-path") == [["PATH", "$venv/bin"], ["PATH", "/my/custom/path"]]
    assert get_setting(text, "append-path") == [["OTHER_VARIABLE", "/my/custom/path2"]]

    assert requirements == ["python/3.7", "my_module"]


def get_setting(text: str, key: str) -> list[tuple[str, str]]:
    environments = []
    for line in text.splitlines():
        if line.startswith(key):
            environments.append(line.split()[1:])

    return environments
