import json
import logging

from pytest import fixture

from datasphere.pyenv import PythonEnv, get_auto_py_env


@fixture
def main_script_path():
    return 'main.py'


@fixture
def namespace():
    return {'foo': 'bar'}


@fixture
def get_module_namespace_mock(mocker, namespace):
    get_module_namespace = mocker.patch('datasphere.pyenv._get_module_namespace')
    get_module_namespace.return_value = namespace
    return get_module_namespace


@fixture
def auto_py_env_mock(mocker):
    auto_py_env = mocker.patch('datasphere.pyenv.AutoPythonEnv')()
    auto_py_env.get_python_version.return_value = '3.11'
    auto_py_env.get_local_module_paths.return_value = ['lib.py']
    auto_py_env.get_pypi_packages.return_value = {'tensorflow-macos': '1.14.0', 'pandas': '2.0'}
    return auto_py_env


def assert_mocks_calls(get_module_namespace, auto_py_env, main_script_path, namespace):
    get_module_namespace.assert_called_once_with(main_script_path)

    auto_py_env.get_python_version.assert_called_once()
    auto_py_env.get_local_module_paths.assert_called_once_with(namespace)
    auto_py_env.get_pypi_packages.assert_called_once_with(namespace)


def test_get_auto_py_env(get_module_namespace_mock, auto_py_env_mock, main_script_path, namespace):
    py_env = get_auto_py_env('main.py')

    assert_mocks_calls(get_module_namespace_mock, auto_py_env_mock, main_script_path, namespace)

    assert py_env == PythonEnv(
        python_version='3.11',
        local_modules_paths=['lib.py'],
        pypi_packages={'tensorflow-macos': '1.14.0', 'pandas': '2.0'},
    )


def test_get_auto_py_env_with_extra(
        get_module_namespace_mock,
        auto_py_env_mock,
        main_script_path,
        namespace,
        mocker,
        tmp_path,
        caplog,
):
    extra_file = tmp_path / 'extra.json'
    extra_file.write_text(json.dumps({
        'package_mapping': {
            'tensorflow-macos': 'tensorflow',
        }
    }))

    getenv = mocker.patch('os.getenv')
    getenv.return_value = str(extra_file)

    caplog.set_level(logging.DEBUG)

    py_env = get_auto_py_env('main.py')

    getenv.assert_called_once_with('PYENV_EXTRA')

    assert_mocks_calls(get_module_namespace_mock, auto_py_env_mock, main_script_path, namespace)

    assert py_env == PythonEnv(
        python_version='3.11',
        local_modules_paths=['lib.py'],
        pypi_packages={'tensorflow': '1.14.0', 'pandas': '2.0'},
    )

    assert caplog.record_tuples == [
        ('datasphere.pyenv', 10,
         f'applying python env extra from `{str(extra_file)}`, '
         "python env before: PythonEnv(python_version='3.11', "
         "local_modules_paths=['lib.py'], pypi_packages={'pandas': '2.0', "
         "'tensorflow': '1.14.0'})")
    ]
