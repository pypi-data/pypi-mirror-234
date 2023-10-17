from pathlib import Path

import pytest

from hatch_modulefile.inputs import ModulefileInputs

INPUTS_WITH_EXTRAS = {
    "requires": ["test"],
    "extra-paths": [{"type": "setenv", "variable": "QT_XCB_GL_INTEGRATION", "value": "none"}],
}

INPUTS_WITH_MODULEFILE = {
    "modulefile_path": "custom_modulefile",
}
INPUTS_WITH_EXTRAS_AND_MODULEFILE = {
    "requires": ["test"],
    "extra-paths": [{"type": "setenv", "variable": "QT_XCB_GL_INTEGRATION", "value": "none"}],
    "modulefile_path": "custom_modulefile",
}

ROOT_DIRECTORY = Path(__file__).parent


def test_read_inputs_extras():
    inputs = ModulefileInputs(INPUTS_WITH_EXTRAS, ROOT_DIRECTORY)
    assert inputs.requires == INPUTS_WITH_EXTRAS["requires"]
    assert inputs.extra_paths == INPUTS_WITH_EXTRAS["extra-paths"]
    assert inputs.modulefile_path is None


def test_read_inputs_specified_modulefile():
    inputs = ModulefileInputs(INPUTS_WITH_MODULEFILE, ROOT_DIRECTORY)
    assert inputs.requires == []
    assert inputs.extra_paths == []
    assert inputs.modulefile_path == ROOT_DIRECTORY.joinpath(INPUTS_WITH_MODULEFILE["modulefile_path"])


def test_read_inputs_specified_modulefile_and_extras():
    with pytest.raises(ValueError, match="Cannot combine requires/extra_paths with modulefile_path"):
        ModulefileInputs(INPUTS_WITH_EXTRAS_AND_MODULEFILE, ROOT_DIRECTORY)
