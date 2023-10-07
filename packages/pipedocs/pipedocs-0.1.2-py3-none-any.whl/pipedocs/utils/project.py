import os
import warnings
from importlib import import_module
from pathlib import Path

from pipedocs.settings import Settings
from pipedocs.utils.conf import closest_pipedocs_cfg, get_config, init_env

ENVVAR = "PIPEDOCS_SETTINGS_MODULE"

def inside_project():
    pipedocs_module = os.environ.get("PIPEDOCS_SETTINGS_MODULE")
    if pipedocs_module is not None:
        try:
            import_module(pipedocs_module)
        except ImportError as exc:
            warnings.warn(
                f"Cannot import pipedocs settings module {pipedocs_module}: {exc}"
            )
        else:
            return True
    #return bool(closest_pipedocs_cfg())
    return False

def get_project_settings():
    if ENVVAR not in os.environ:
        project = os.environ.get("PIPEDOCS_PROJECT", "default")
        init_env(project)

    settings = Settings()
    settings_module_path = os.environ.get(ENVVAR)
    if settings_module_path:
        settings.setmodule(settings_module_path, priority="project")

    valid_envvars = {
        "CHECK",
        "PROJECT",
        "PYTHON_SHELL",
        "SETTINGS_MODULE",
    }

    pipedocs_envvars = {
        k[7:]: v
        for k, v in os.environ.items()
        if k.startswith("PIPEDOCS_") and k.replace("PIPEDOCS_", "") in valid_envvars
    }

    settings.setdict(pipedocs_envvars, priority="project")

    return settings