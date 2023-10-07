from dataclasses import dataclass
import importlib
import logging
import os
import sys
from typing import Dict, Any

from lzy.env.explorer.base import ModulePathsList, PackagesDict
from lzy.env.python.auto import AutoPythonEnv
import yaml

logger = logging.getLogger(__name__)


@dataclass
class PythonEnv:
    python_version: str
    local_modules_paths: ModulePathsList
    pypi_packages: PackagesDict


def get_auto_py_env(main_script_path: str) -> PythonEnv:
    # User may not add cwd to PYTHONPATH, in case of running execution through `datasphere`, not `python -m`.
    # Since path to python script can be only relative, this should always work.
    sys.path.append(os.getcwd())
    namespace = _get_module_namespace(main_script_path)

    provider = AutoPythonEnv()
    return PythonEnv(
        python_version=provider.get_python_version(),
        local_modules_paths=provider.get_local_module_paths(namespace),
        pypi_packages=provider.get_pypi_packages(namespace),
    )


def _get_module_namespace(path: str) -> Dict[str, Any]:
    module_spec = importlib.util.spec_from_file_location('module', path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return vars(module)


# Copy-pasted from LzyCall.generate_conda_config()
def get_conda_yaml(py_env: PythonEnv) -> str:
    python_version = py_env.python_version
    dependencies = [f'python=={python_version}', 'pip']

    libraries = [f'{name}=={version}' for name, version in py_env.pypi_packages.items()]
    if libraries:
        dependencies.append({'pip': libraries})

    return yaml.dump({'name': 'default', 'dependencies': dependencies}, sort_keys=False)
