from dataclasses import dataclass, field
from functools import partial
from io import StringIO
import logging
from pathlib import Path
from re import compile
from typing import BinaryIO, TextIO, Callable, Dict, List, Optional, Union
import yaml

from yandex.cloud.datasphere.v2.jobs.jobs_pb2 import (
    FileDesc,
    File,
    DockerImageSpec,
    Environment as EnvironmentProto,
    PythonEnv as PythonEnvProto,
    JobParameters,
    CloudInstanceType,
)
from datasphere.utils import get_sha256_and_size, humanize_bytes_size
from datasphere.pyenv import PythonEnv, get_conda_yaml

logger = logging.getLogger(__name__)


@dataclass
class VariablePath:
    path: str
    var: Optional[str] = None

    _file: File = field(init=False, default=None)

    @property
    def file_desc(self) -> FileDesc:
        return FileDesc(path=self.path, var=self.var)

    def get_file(self, f: Optional[BinaryIO] = None) -> File:
        # TODO: one can call get_file() then get_file(f) on single file; fix semantics
        if self._file:
            return self._file

        if f:
            self._file = self._read_file(f)
        else:
            with open(self.path, 'rb') as f:
                self._file = self._read_file(f)
        return self._file

    def _read_file(self, f: BinaryIO) -> File:
        sha256, size = get_sha256_and_size(f)
        return File(desc=self.file_desc, sha256=sha256, size_bytes=size)


@dataclass
class Password:
    text: str
    is_secret: bool


@dataclass
class DockerImage:
    url: str
    username: Optional[str]
    password: Optional[Password]

    @property
    def proto(self) -> DockerImageSpec:
        spec = DockerImageSpec()
        spec.image_url = self.url
        username = self.username
        if username is not None:
            spec.username = username
        password = self.password
        if password is not None:
            if password.is_secret:
                spec.password_ds_secret_name = password.text
            else:
                spec.password_plain_text = password.text
        return spec


@dataclass
class PythonEnv:
    auto: bool = True


@dataclass
class Environment:
    vars: Optional[Dict[str, str]]
    docker_image: Optional[Union[str, DockerImage]]  # Image resource ID or image URL
    python: Optional[PythonEnv]


@dataclass
class Config:
    cmd: str
    inputs: List[VariablePath]
    outputs: List[VariablePath]
    s3_mounts: List[VariablePath]
    datasets: List[VariablePath]
    env: Environment
    cloud_instance_type: str
    attach_project_disk: bool
    content: str
    name: Optional[str] = None
    desc: Optional[str] = None

    python_script: Optional[str] = field(init=False, default=None)

    def __post_init__(self):
        def get_vars(paths: List[VariablePath], with_non_vars: bool = False) -> List[str]:
            result = [v.var for v in paths if v.var is not None]
            if with_non_vars:
                result += [v.path for v in paths]
            return result

        self.__vars = \
            get_vars(self.inputs) + get_vars(self.outputs) + \
            get_vars(self.s3_mounts, with_non_vars=True) + get_vars(self.datasets, with_non_vars=True)

        if len(self.__vars) != len(set(self.__vars)):
            raise ValueError('variables in config should be unique')  # TODO: test; display non-unique

        # If section `env.python` exists, then user runs Python, and we add main script to `inputs` automatically.
        # If `env.python` is absent, then user runs arbitrary binary executable or shell script file and user has to add
        # this file to `inputs` manually.

        if self.env.python is not None:
            self.python_script = self._python_script()
            self.inputs = list(self.inputs) + [VariablePath(path=self.python_script)]  # do not modify source list

    @property
    def vars(self) -> List[str]:
        return self.__vars

    def _python_script(self) -> str:
        # Python script is passed as input file. Its path can be only relative in cwd to avoid its substitution in cmd.
        # If non-relative in cwd script path will become a common use case, we can use reserved variable for it.
        # First word in cmd is supposed to be Python interpreter file, but we're ignoring it.
        try:
            path = self.cmd.split(' ')[1]
        except IndexError:
            raise ValueError('you have to specify path to python script in `cmd`')
        logger.debug('`%s` is parsed as python script path', path)
        return path

    def get_job_params(self, py_env: Optional[PythonEnv], local_modules: List[File]) -> JobParameters:
        env = EnvironmentProto(
            vars=self.env.vars,
            python_env=PythonEnvProto(
                # If `auto: true` is not set, we use collected python env only to transfer local modules,
                # considering required pypi packages will be in docker or be manually specified.
                conda_yaml=get_conda_yaml(py_env),  # if self.env.python.auto else '',  TODO: uncomment after server fix
                local_modules=local_modules,
            ) if py_env else None
        )
        docker_image = self.env.docker_image
        if docker_image:
            if isinstance(docker_image, str):
                env.docker_image_resource_id = docker_image
            else:
                env.docker_image_spec.CopyFrom(docker_image.proto)

        return JobParameters(
            input_files=[f.get_file() for f in self.inputs],
            output_files=[f.file_desc for f in self.outputs],
            s3_mount_ids=[p.path for p in self.s3_mounts],
            dataset_ids=[p.path for p in self.datasets],
            cmd=self.cmd,
            env=env,
            attach_project_disk=self.attach_project_disk,
            cloud_instance_type=CloudInstanceType(name=self.cloud_instance_type),
        )


PathValidatorType = Callable[[VariablePath], str]


def parse_variable_path_list(
        config: dict,
        key: str,
        validator: Optional[PathValidatorType] = None,
) -> List[VariablePath]:
    value_list = config.get(key, [])
    if not isinstance(value_list, list):
        raise ValueError(f'`{key}` should be a list')
    result = []
    for value in value_list:
        try:
            result.append(get_variable_path(value, validator))
        except ValueError as e:
            raise ValueError(f'invalid `{key}` entry: `{value}`: {e}')
    return result


VariablePathType = Union[str, Dict[str, str], Dict[str, Dict[str, str]]]

var_pattern = compile(r'[0-9a-z-A-z\-_]{1,50}')
ds_project_home = 'DS_PROJECT_HOME'
py_script_path = 'PY_SCRIPT'
reserved_vars = {ds_project_home}
local_module_prefix = '_LOCAL_MODULE'  # not reserved since such name is invalid by pattern


def get_variable_path(
        value: VariablePathType,
        validator: Optional[PathValidatorType] = None,
) -> VariablePath:
    result = parse_variable_path(value)
    if result.var and not var_pattern.fullmatch(result.var):
        raise ValueError(f'var `{result.var}` does not fit regexp {var_pattern.pattern}')
    if result.var in reserved_vars:
        raise ValueError(f'name `{result.var}` is reserved and cannot be used for variable')
    path_err = validator(result)
    if path_err:
        raise ValueError(f'value is incorrect: {path_err}')
    return result


def parse_variable_path(path: VariablePathType) -> VariablePath:
    if isinstance(path, str):
        return VariablePath(path=path)
    elif isinstance(path, dict):
        if len(path) != 1:
            raise ValueError('multiple items in dict')
        k = next(iter(path))
        v = path[k]
        if isinstance(v, str):
            return VariablePath(path=k, var=v)
        elif isinstance(v, dict):
            if list(v.keys()) != ['var']:
                raise ValueError('only `var` param is supported')
            return VariablePath(path=k, var=v['var'])
        else:
            raise ValueError('invalid dict value')
    else:
        raise ValueError('not a string or dict')


def parse_docker_image(env: Optional[dict]) -> Optional[Union[str, DockerImage]]:
    if 'docker' not in env:
        return None
    docker = env['docker']
    if isinstance(docker, str):
        return get_resource_id(docker, 'error in docker image ID')
    elif isinstance(docker, dict):
        url = docker['image']
        username = docker.get('username')
        password_data = docker.get('password')
        password = None
        if password_data:
            if isinstance(password_data, dict) and 'secret-id' in password_data:
                password = Password(password_data['secret-id'], is_secret=True)
            elif isinstance(password_data, str):
                password = Password(password_data, is_secret=False)
            else:
                raise ValueError(f'unexpected value for docker password: {password_data}')
        return DockerImage(url, username, password)
    else:
        raise ValueError(f'invalid docker image format: {docker}')


def parse_python_env(env: Optional[dict]) -> Optional[PythonEnv]:
    if 'python' not in env:
        return None
    python = env['python']
    if not isinstance(python, dict):
        raise ValueError(f'invalid python env format: {python}')
    auto_py_env = python.get('auto', 'true').lower() in ['true', 't', 'yes', 'y']
    return PythonEnv(auto=auto_py_env)


def parse_env(env: Optional[dict]) -> Environment:
    if env is None:
        return Environment(vars=None, docker_image=None, python=None)
    env_vars = env.get('vars')
    if env_vars and (not isinstance(env_vars, dict) or any(
            not isinstance(x, str)
            for x in list(env_vars.keys()) + list(env_vars.values())
    )):
        raise ValueError('environment vars should be a dict[str, str]')
    return Environment(env_vars, parse_docker_image(env), parse_python_env(env))


def validate_path(v: VariablePath, is_input: bool) -> str:
    p = Path(v.path)
    if is_input and not p.exists():
        return f'no such path: {p}'
    if is_input and p.is_dir():
        return f'{p} is a directory'
    is_relative = not p.is_absolute() and '..' not in p.as_posix()
    if not v.var and not is_relative:
        return f'path without variable should be relative: {p}'
    return ''


validate_input_path = partial(validate_path, is_input=True)
validate_output_path = partial(validate_path, is_input=False)

resource_id_pattern = compile(r'[0-9a-z]{20}')


def is_resource_id(s: str) -> bool:
    return isinstance(s, str) and resource_id_pattern.fullmatch(s)


def validate_resource_id(v: VariablePath) -> str:
    if not is_resource_id(v.path):
        return f'invalid resource ID: {v.path}'
    return ''


def get_resource_id(s: str, err_msg: str) -> str:
    err = validate_resource_id(VariablePath(path=s))
    if err:
        raise ValueError(f'{err_msg}: {err}')
    return s


# may be use string.Template for that
var_tpl_pattern = compile(r'\$\{(.+?)}')


def process_cmd(config: Config) -> str:
    raw_cmd = config.cmd
    if len(raw_cmd) == 0:
        raise ValueError('empty `cmd`')
    var_to_resource_id = {x.var: x.path for x in (config.s3_mounts + config.datasets)}
    cmd = raw_cmd
    for var in var_tpl_pattern.findall(cmd):
        if var in reserved_vars:
            continue
        if var not in config.vars:
            raise ValueError(f'`cmd` contains variable not presented in config: {var}')
        if var in var_to_resource_id:
            cmd = cmd.replace(var, var_to_resource_id[var])
    if not config.attach_project_disk and ('${%s}' % ds_project_home) in raw_cmd:
        raise ValueError(f'{ds_project_home} is unavailable since you did not add `attach-project-disk` option')
    return cmd


def parse_config(f: Union[Path, TextIO]) -> Config:
    if isinstance(f, Path):
        config_str = f.read_text()
    else:
        config_str = f.read()
    config_dict = yaml.load(StringIO(config_str), Loader=yaml.BaseLoader)
    if config_dict is None or len(config_dict) == 0:
        raise ValueError('config is empty')
    for opt in ('cmd',):
        if opt not in config_dict:
            raise ValueError(f'`{opt}` is required')
    flags = config_dict.get('flags', [])
    if not isinstance(flags, list):
        raise ValueError('`flags` should be a list')
    config = Config(
        name=config_dict.get('name'),
        desc=config_dict.get('desc'),
        cmd=config_dict['cmd'],
        inputs=parse_variable_path_list(config_dict, 'inputs', validate_input_path),
        outputs=parse_variable_path_list(config_dict, 'outputs', validate_output_path),
        s3_mounts=parse_variable_path_list(config_dict, 's3-mounts', validate_resource_id),
        datasets=parse_variable_path_list(config_dict, 'datasets', validate_resource_id),
        env=parse_env(config_dict.get('env')),
        cloud_instance_type=config_dict.get('cloud-instance-type', 'c1.4'),
        attach_project_disk='attach-project-disk' in flags,
        content=config_str,
    )
    config.cmd = process_cmd(config).strip()
    return config


UPLOAD_FILE_MAX_SIZE_BYTES = 5 * (1 << 30)  # 5Gb
UPLOAD_FILES_MAX_TOTAL_SIZE_BYTES = 10 * (1 << 30)  # 10Gb
FILES_LIST_MAX_SIZE = 100


def check_limits(config: Config, local_modules: List[File]):
    upload_files_size_bytes = 0
    for f in [path.get_file() for path in config.inputs] + local_modules:
        assert f.size_bytes <= UPLOAD_FILE_MAX_SIZE_BYTES, \
            f'size of file {f.desc.path} = {humanize_bytes_size(f.size_bytes)}, ' \
            f'while limit = {humanize_bytes_size(UPLOAD_FILE_MAX_SIZE_BYTES)}'
        upload_files_size_bytes += f.size_bytes

    local_modules_msg = ' and Python local modules' if len(local_modules) else ''
    assert upload_files_size_bytes <= UPLOAD_FILES_MAX_TOTAL_SIZE_BYTES, \
        f'total size of input files{local_modules_msg} = {humanize_bytes_size(upload_files_size_bytes)}, ' \
        f'while limit = {humanize_bytes_size(UPLOAD_FILES_MAX_TOTAL_SIZE_BYTES)} bytes.'
    for entries, name in (
            (config.inputs, 'input files'),
            (config.outputs, 'output files'),
            (config.s3_mounts, 's3 mounts'),
            (config.datasets, 'datasets'),
    ):
        assert len(entries) <= FILES_LIST_MAX_SIZE, f'number of {name} must be not greater than {FILES_LIST_MAX_SIZE}'
