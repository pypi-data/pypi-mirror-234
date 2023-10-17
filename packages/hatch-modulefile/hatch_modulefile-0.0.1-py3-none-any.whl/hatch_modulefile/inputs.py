from __future__ import annotations

import platform
from pathlib import Path


class ModulefileInputs:
    def __init__(self, inputs: dict[str, str], root_directory: Path) -> None:
        self.inputs = inputs
        self.root_directory = root_directory

        self.validate()

    def generate_modulefile_string(self) -> str:
        """Generates a modulefile and returns a string ready to write to file.

        Returns
        -------
        str
            Modulefile inputs
        """
        return MODULEFILE_TEMPLATE.format(
            python_version=platform.python_version().rsplit(".", 1)[0],
            requires_string=self.get_requires_string(),
            extra_paths_string=self.get_extra_paths_string(),
        )

    def get_extra_paths_string(self) -> str:
        """Convert TOML inputs for tool.pydev.modulefile.extra-paths into a single
        string with one new line per entry

        Parameters
        ----------
        extra_paths : List[Dict[str, str]]
            List of extra path inputs

        Returns
        -------
        str
            Single string with environment paths combined by newlines
        """
        types = {
            "append": "append-path",
            "prepend": "prepend-path",
            "append-path": "append-path",
            "prepend-path": "prepend-path",
            "setenv": "setenv",
        }
        all_strings = []
        for entry in self.extra_paths:
            entry_type = entry["type"]
            variable = entry["variable"]
            value = entry["value"]

            # Try and convert a common name to the TCL requirement
            if entry_type not in types:
                validated_type = entry_type
            else:
                validated_type = types[entry_type]

            all_strings.append(f"{validated_type.ljust(15)} {variable.ljust(23)} {value}")

        if all_strings:
            all_strings.insert(0, "\n# Extra module path requirements")

        return "\n".join(all_strings)

    def get_requires_string(self) -> str:
        """Returns a formatted string for inserting into the modulefile template.

        Returns
        -------
        str
            String containing all required modules separated by tabs and newlines.
        """
        return "\n\t".join(self.requires)

    def validate(self):
        """Validates inputs for modulefile generation

        Raises
        ------
        ValueError
            Cannot combine requires/extra_paths with modulefile_path
        """
        if (self.requires or self.extra_paths) and self.modulefile_path:
            msg = "Cannot combine requires/extra_paths with modulefile_path"
            raise ValueError(msg)

    @property
    def requires(self) -> list[str]:
        return self.inputs.get("requires", [])

    @property
    def extra_paths(self) -> list[str]:
        return self.inputs.get("extra-paths", [])

    @property
    def modulefile_path(self):
        path = self.inputs.get("modulefile_path", None)
        if path:
            return self.root_directory.joinpath(path).resolve()


MODULEFILE_TEMPLATE = """#%Module

# Gets the folder two folders up from this file
set             venv                    [file dirname [file dirname [file dirname [file normalize $ModulesCurrentModulefile/___]]]]

# Standard python path requirements
prepend-path	 PATH $venv/bin
setenv		     PYTHON_ROOT $venv
{extra_paths_string}

set     necessary       {{
\t{requires_string}
}}

foreach mod $necessary {{
\tset splitList [split $mod "/"]
\tset mod_name [lindex $splitList 0]
\tif {{ [ is-loaded $mod_name ] }} {{
\t\tmodule switch $mod
\t}} else {{
\t\tmodule load $mod
\t}}
}}

"""  # noqa: E501


def get_all(inputs: dict[str, str], keys: list[str]) -> dict[str, str] | str:
    for key in keys:
        if key not in inputs:
            return {}
        inputs = inputs[key]

    return inputs
