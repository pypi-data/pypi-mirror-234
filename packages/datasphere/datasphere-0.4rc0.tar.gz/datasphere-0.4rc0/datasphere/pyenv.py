from dataclasses import dataclass
import importlib
import json
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
    py_env = PythonEnv(
        python_version=provider.get_python_version(),
        local_modules_paths=provider.get_local_module_paths(namespace),
        pypi_packages=provider.get_pypi_packages(namespace),
    )

    _apply_package_mapping(py_env)
    return py_env


# Some packages like `tensorflow` have platform-specific subpackages like `tensorflow-intel` for Windows or
# `tensorflow-macos` for macOS M1. On server, we want to install `tensorflow`. In its next version pylzy will perform
# such mapping finding platform-specific packages by their tags and finding their meta-package, for now it's a
# quickfix and workaround in case if pylzy fix won't cover all such cases.
def _apply_package_mapping(py_env: PythonEnv):
    # File with custom things which will be applied to collected pyenv.
    extra_file = os.getenv('PYENV_EXTRA')
    if not extra_file:
        return
    logger.debug('applying python env extra from `%s`, python env before: %s', extra_file, py_env)
    with open(extra_file) as f:
        extra = json.load(f)
    packages = py_env.pypi_packages
    for from_name, to_name in extra.get('package_mapping', {}).items():
        version = packages.get(from_name)
        if version:
            packages[to_name] = version
            del packages[from_name]


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
