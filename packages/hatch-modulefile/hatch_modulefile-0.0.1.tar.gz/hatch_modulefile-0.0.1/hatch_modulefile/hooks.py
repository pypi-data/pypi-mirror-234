from hatchling.plugin import hookimpl

from hatch_modulefile.plugins import ModulefileBuildHook


@hookimpl
def hatch_register_build_hook():
    return ModulefileBuildHook
