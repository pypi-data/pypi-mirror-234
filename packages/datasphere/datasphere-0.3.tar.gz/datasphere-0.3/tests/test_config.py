from pathlib import Path
import re
from typing import List

from pytest import raises, fixture

import datasphere.config
from datasphere.config import (
    validate_resource_id,
    validate_path,
    validate_input_path,
    parse_variable_path,
    VariablePath,
    get_variable_path,
    parse_variable_path_list,
    DockerImage,
    Password,
    parse_docker_image,
    PythonEnv,
    parse_python_env,
    Environment,
    parse_env,
    process_cmd,
    Config,
    parse_config,
    check_limits,
)
from yandex.cloud.datasphere.v2.jobs.jobs_pb2 import DockerImageSpec, File


@fixture
def input_file():
    path = Path('input.txt')
    path.write_text('foo')
    yield str(path)
    path.unlink()


def test_validate_resource_id():
    assert validate_resource_id(VariablePath(path='foo')) == 'invalid resource ID: foo'
    assert validate_resource_id(VariablePath(path='bt10gr4c1b081bidoses')) == ''


def test_validate_path(tmp_path, input_file):
    assert validate_path(VariablePath(path='foobar.pdf'), is_input=True) == 'no such path: foobar.pdf'
    cur_dir = str(Path(__file__).parent.absolute())
    assert validate_path(VariablePath(path=cur_dir), is_input=True) == f'{cur_dir} is a directory'
    assert validate_path(VariablePath(path='../setup.py'), is_input=False) == \
           'path without variable should be relative: ../setup.py'

    f = tmp_path / 'foo.txt'
    f.write_text('bar')
    assert validate_path(VariablePath(path=str(f.absolute())), is_input=True) == \
           f'path without variable should be relative: {f.absolute()}'

    assert validate_path(VariablePath(path='foobar.pdf'), is_input=False) == ''
    assert validate_path(VariablePath(path=input_file), is_input=True) == ''
    assert validate_path(VariablePath(path=str(f.absolute()), var='PARAMS'), is_input=True) == ''


def test_parse_variable_value():
    assert parse_variable_path('misc/logging.yaml') == VariablePath('misc/logging.yaml')
    assert parse_variable_path({'data/model.bin': 'MODEL'}) == VariablePath('data/model.bin', 'MODEL')
    assert parse_variable_path(
        {'/usr/share/params.json': {'var': 'PARAMS'}}
    ) == VariablePath('/usr/share/params.json', 'PARAMS')

    with raises(ValueError, match='not a string or dict'):
        parse_variable_path(42)  # noqa

    with raises(ValueError, match='multiple items in dict'):
        parse_variable_path({'data/model.bin': '', 'var': 'MODEL'})

    with raises(ValueError, match='only `var` param is supported'):
        parse_variable_path({'/usr/share/params.json': {'foo': 'bar'}})

    with raises(ValueError, match='invalid dict value'):
        parse_variable_path({'/usr/share/params.json': 42})  # noqa


def test_get_variable_value():
    with raises(ValueError, match='var `!foo.j` does not fit regexp [0-9a-z-A-z\\-_]{1,50}'):
        get_variable_path({'/usr/share/params.json': {'var': '!foo.j'}})

    with raises(ValueError, match='value is incorrect: invalid resource ID: foo'):
        get_variable_path('foo', validate_resource_id)

    with raises(ValueError, match='name `DS_PROJECT_HOME` is reserved and cannot be used for variable'):
        get_variable_path({'data/model.bin': 'DS_PROJECT_HOME'})


def test_parse_variable_value_list():
    with raises(ValueError, match='`inputs` should be a list'):
        parse_variable_path_list({'inputs': {'foo': 'bar'}}, 'inputs')

    with raises(ValueError, match='invalid `inputs` entry: `foobar.pdf`: value is incorrect: no such path: foobar.pdf'):
        parse_variable_path_list({'inputs': ['foobar.pdf']}, 'inputs', validate_input_path)



@fixture
def docker_image_with_plain_password_dict() -> dict:
    return {
        'docker': {
            'image': 'cr.yandex/crtabcdef12345678900/myenv:0.1',
            'username': 'foo',
            'password': 'bar',
        }
    }


@fixture
def docker_image_with_plain_password() -> DockerImage:
    return DockerImage(
        url='cr.yandex/crtabcdef12345678900/myenv:0.1',
        username='foo',
        password=Password(text='bar', is_secret=False),
    )


@fixture
def docker_image_with_secret_password_no_username_dict() -> dict:
    return {
        'docker': {
            'image': 'ubuntu:focal',
            'password': {'secret-id': 'CR_PASSWORD'},
        }
    }


@fixture
def docker_image_with_secret_password_no_username() -> DockerImage:
    return DockerImage(
        url='ubuntu:focal',
        username=None,
        password=Password(text='CR_PASSWORD', is_secret=True),
    )


def test_parse_docker_image(
        docker_image_with_plain_password_dict,
        docker_image_with_plain_password,
        docker_image_with_secret_password_no_username_dict,
        docker_image_with_secret_password_no_username,
):
    assert parse_docker_image({'inputs': []}) is None

    assert parse_docker_image({'docker': 'b1gldgej4sak01tcg79m'}) == 'b1gldgej4sak01tcg79m'

    assert parse_docker_image(docker_image_with_plain_password_dict) == docker_image_with_plain_password
    assert docker_image_with_plain_password.proto == DockerImageSpec(
        image_url='cr.yandex/crtabcdef12345678900/myenv:0.1',
        username='foo',
        password_plain_text='bar',
    )

    assert parse_docker_image(docker_image_with_secret_password_no_username_dict) == \
           docker_image_with_secret_password_no_username
    assert docker_image_with_secret_password_no_username.proto == DockerImageSpec(
        image_url='ubuntu:focal',
        username=None,
        password_ds_secret_name='CR_PASSWORD',
    )

    with raises(ValueError, match='invalid docker image format: 42'):
        parse_docker_image({'docker': 42})

    with raises(ValueError, match='error in docker image ID: invalid resource ID: ubuntu:focal'):
        parse_docker_image({'docker': 'ubuntu:focal'})

    with raises(ValueError, match="unexpected value for docker password: {'secret': 'CR_PASSWORD'}"):
        parse_docker_image({'docker': {
            'image': 'ubuntu:focal',
            'password': {'secret': 'CR_PASSWORD'},
        }})

    with raises(ValueError, match='unexpected value for docker password: 12345'):
        parse_docker_image({'docker': {
            'image': 'ubuntu:focal',
            'password': 12345,
        }})


def test_parse_python_env():
    assert parse_python_env({}) is None
    assert parse_python_env({'python': {'auto': 'false'}}) == PythonEnv(auto=False)
    assert parse_python_env({'python': {'auto': 'yes'}}) == PythonEnv(auto=True)
    assert parse_python_env({'python': {'auto': 'True'}}) == PythonEnv(auto=True)
    assert parse_python_env({'python': {'some_opt': 42}}) == PythonEnv(auto=True)

    with raises(ValueError, match='invalid python env format: True'):
        parse_python_env({'python': True})


def test_parse_env(
        docker_image_with_secret_password_no_username_dict,
        docker_image_with_secret_password_no_username,
):
    assert parse_env(None) == Environment(vars=None, docker_image=None, python=None)

    assert parse_env({
        'docker': 'b1gldgej4sak01tcg79m',
        'python': {'auto': 'False'},
    }) == Environment(
        vars=None,
        docker_image='b1gldgej4sak01tcg79m',
        python=PythonEnv(auto=False),
    )

    assert parse_env({
        'vars': {'FOO': 'bar'},
        **docker_image_with_secret_password_no_username_dict,
    }) == Environment(
        vars={'FOO': 'bar'},
        docker_image=docker_image_with_secret_password_no_username,
        python=None,
    )

    with raises(ValueError, match=re.escape('environment vars should be a dict[str, str]')):
        parse_env({'vars': 42})

    with raises(ValueError, match=re.escape('environment vars should be a dict[str, str]')):
        parse_env({'vars': {'foo': 42}})

    with raises(ValueError, match=re.escape('environment vars should be a dict[str, str]')):
        parse_env({'vars': {42: 'foo'}})


def test_parse_config_errors(tmp_path):
    cfg = tmp_path / 'cfg1.yaml'
    cfg.write_text('')
    with raises(ValueError, match='config is empty'):
        parse_config(cfg.absolute())

    cfg = tmp_path / 'cfg2.yaml'
    cfg.write_text("""
name: foo
    """)
    with raises(ValueError, match='`cmd` is required'):
        parse_config(cfg.absolute())

    cfg = tmp_path / 'cfg3.yaml'
    cfg.write_text("""
cmd: python src/main.py
flags: 
  attach-project-disk: true
    """)
    with raises(ValueError, match='`flags` should be a list'):
        parse_config(cfg.absolute())

    params = tmp_path / 'params.json'
    params.write_text("{}")

    cfg = tmp_path / 'cfg4.yaml'
    cfg.write_text(f"""
cmd: python src/main.py
inputs:
  - {params.absolute()}:
      var: DATA
datasets:
  - bt12tlsc3nkt2opg2h61:
      var: DATA
    """)
    with raises(ValueError, match='variables in config should be unique'):
        parse_config(cfg.absolute())


def test_process_cmd():
    cfg = Config(
        cmd="""
python src/main.py 
  --params ${PARAMS}
  --features ${DATA}/features.tsv 
  --validate ${CIFAR}/val.json
  --normalizer ${DS_PROJECT_HOME}/misc/norm.bin
  --model ${MODEL}
  --foo ${CIFAR}/${DATA}/bar.txt
  --baz ${bt12tlsc3nkt2opg2h61}/bob.txt
  --epochs 5
        """.strip(),
        inputs=[
            VariablePath(path='misc/logging.yaml'),
            VariablePath(path='/usr/share/params.json', var='PARAMS'),
        ],
        outputs=[
            VariablePath(path='data/model.bin', var='MODEL'),
            VariablePath(path='other/metrics.png'),
        ],
        s3_mounts=[],
        datasets=[
            VariablePath(path='bt12tlsc3nkt2opg2h61', var='CIFAR'),
        ],
        env=Environment(vars=None, docker_image=None, python=PythonEnv(auto=True)),
        cloud_instance_type='c1.4',
        attach_project_disk=False,
        content='nevermind',
    )

    with raises(ValueError, match='`cmd` contains variable not presented in config: DATA'):
        process_cmd(cfg)

    cfg.s3_mounts = [VariablePath(path='bt10gr4c1b081bidoses', var='DATA')]
    cfg.__post_init__()

    with raises(ValueError, match='DS_PROJECT_HOME is unavailable since you did not add `attach-project-disk` option'):
        process_cmd(cfg)


    cfg.attach_project_disk = True
    cmd = process_cmd(cfg)

    assert cmd == """
python src/main.py 
  --params ${PARAMS}
  --features ${bt10gr4c1b081bidoses}/features.tsv 
  --validate ${bt12tlsc3nkt2opg2h61}/val.json
  --normalizer ${DS_PROJECT_HOME}/misc/norm.bin
  --model ${MODEL}
  --foo ${bt12tlsc3nkt2opg2h61}/${bt10gr4c1b081bidoses}/bar.txt
  --baz ${bt12tlsc3nkt2opg2h61}/bob.txt
  --epochs 5
        """.strip()


def test_parse_config(
        tmp_path,
        docker_image_with_plain_password,
        docker_image_with_secret_password_no_username,
        input_file,
):
    params_f = tmp_path / 'params.json'
    params_f.write_text('{}')

    cfg_f = tmp_path / 'cfg1.yaml'
    cfg_f.write_text(f"""
name: my-script
desc: Learning model using PyTorch
cmd: >  # YAML multiline string
  python src/main.py 
    --params ${{PARAMS}}
    --features ${{bt10gr4c1b081bidoses}}/features.tsv 
    --validate ${{CIFAR}}/val.json
    --normalizer ${{DS_PROJECT_HOME}}/misc/norm.bin
    --model ${{MODEL}}
    --epochs 5
inputs:
  - {input_file}
  - {params_f.absolute()}:
      var: PARAMS
outputs:
  - data/model.bin: MODEL
  - other/metrics.png
s3-mounts:
  - bt10gr4c1b081bidoses
datasets:
  - bt12tlsc3nkt2opg2h61:
      var: CIFAR
env:
  vars:
    PYTHONBUFFERED: true
    PASSWORD: qwerty
    DEVICE_COUNT: 8
  docker: b1gldgej4sak01tcg79m
  python:
    auto: false
flags:
  - attach-project-disk
cloud-instance-type: g2.8
    """.strip())
    cfg = parse_config(cfg_f.absolute())
    assert cfg == Config(
        name='my-script',
        desc='Learning model using PyTorch',
        cmd="""
python src/main.py 
  --params ${PARAMS}
  --features ${bt10gr4c1b081bidoses}/features.tsv 
  --validate ${bt12tlsc3nkt2opg2h61}/val.json
  --normalizer ${DS_PROJECT_HOME}/misc/norm.bin
  --model ${MODEL}
  --epochs 5
        """.strip(),
        inputs=[
            VariablePath(path=input_file),
            VariablePath(path=str(params_f.absolute()), var='PARAMS'),
        ],
        outputs=[
            VariablePath(path='data/model.bin', var='MODEL'),
            VariablePath(path='other/metrics.png'),
        ],
        s3_mounts=[
            VariablePath(path='bt10gr4c1b081bidoses'),
        ],
        datasets=[
            VariablePath(path='bt12tlsc3nkt2opg2h61', var='CIFAR'),
        ],
        env=Environment(
            vars={'PYTHONBUFFERED': 'true', 'PASSWORD': 'qwerty', 'DEVICE_COUNT': '8'},
            docker_image='b1gldgej4sak01tcg79m',
            python=PythonEnv(auto=False),
        ),
        cloud_instance_type='g2.8',
        attach_project_disk=True,
        content=cfg_f.read_text(),
    )

    cfg_f = tmp_path / 'cfg2.yaml'
    cfg_f.write_text("""
cmd: python run.py
env:
  docker:
    image: cr.yandex/crtabcdef12345678900/myenv:0.1
    username: foo
    password: bar
    """.strip())
    cfg = parse_config(cfg_f.absolute())
    assert cfg == Config(
        name=None,
        desc=None,
        cmd='python run.py',
        inputs=[],
        outputs=[],
        s3_mounts=[],
        datasets=[],
        env=Environment(
            vars=None,
            docker_image=docker_image_with_plain_password,
            python=None,
        ),
        cloud_instance_type='c1.4',
        attach_project_disk=False,
        content=cfg_f.read_text(),
    )

    cfg_f = tmp_path / 'cfg3.yaml'
    cfg_f.write_text("""
name: my-script
cmd: python run.py
env:
  docker:
    image: ubuntu:focal
    password:
       secret-id: CR_PASSWORD
  python:
    auto: true
        """.strip())
    cfg = parse_config(cfg_f.absolute())
    assert cfg == Config(
        name='my-script',
        cmd='python run.py',
        inputs=[],
        outputs=[],
        s3_mounts=[],
        datasets=[],
        env=Environment(
            vars=None,
            docker_image=docker_image_with_secret_password_no_username,
            python=PythonEnv(auto=True),
        ),
        cloud_instance_type='c1.4',
        attach_project_disk=False,
        content=cfg_f.read_text(),
    )


def test_python_script():
    def get_cfg(cmd: str, is_python: bool = True):
        return Config(
            cmd=cmd,
            inputs=[],
            outputs=[],
            s3_mounts=[],
            datasets=[],
            env=Environment(vars=None, docker_image=None, python=PythonEnv(auto=True) if is_python else None),
            cloud_instance_type='c1.4',
            attach_project_disk=False,
            content='nevermind',
        )

    cfg = get_cfg(cmd='python src/main.py --foo bar')
    assert cfg.python_script == 'src/main.py'

    cfg = get_cfg(cmd='foobar run.py')  # We are ignoring first word with Python interpreter file.
    assert cfg.python_script == 'run.py'

    with raises(ValueError, match='you have to specify path to python script in `cmd`'):
        _ = get_cfg(cmd='python')

    cfg = get_cfg(cmd='ls .', is_python=False)
    assert cfg.python_script is None


def test_check_limits(monkeypatch, tmp_path):
    monkeypatch.setattr(datasphere.config, 'UPLOAD_FILE_MAX_SIZE_BYTES', 600)
    monkeypatch.setattr(datasphere.config, 'UPLOAD_FILES_MAX_TOTAL_SIZE_BYTES', 2000)
    monkeypatch.setattr(datasphere.config, 'FILES_LIST_MAX_SIZE', 2)

    paths = []
    for i in range(3):
        f = tmp_path / f'{i}.txt'
        f.write_text(str(i))
        paths.append(VariablePath(str(f)))

    big_f = tmp_path / 'big.txt'
    big_f.write_bytes(b'1' * 512)
    big_path = VariablePath(str(big_f))

    huge_f = tmp_path / 'huge.txt'
    huge_f.write_bytes(b'1' * 700)
    huge_f = VariablePath(str(huge_f))

    def get_cfg(
            inputs: List[VariablePath] = None,
            outputs: List[VariablePath] = None,
            s3_mounts: List[VariablePath] = None,
            datasets: List[VariablePath] = None,
    ):
        return Config(
            cmd=f'python {paths[0].path}',
            inputs=inputs or [],
            outputs=outputs or [],
            s3_mounts=s3_mounts or [],
            datasets=datasets or [],
            env=Environment(vars=None, docker_image=None, python=PythonEnv(auto=True)),
            cloud_instance_type='c1.4',
            attach_project_disk=False,
            content='nevermind',
        )

    with raises(AssertionError, match=f'size of file {huge_f.path} = 700.0B, while limit = 600.0B'):
        check_limits(get_cfg(inputs=[huge_f]), [])
    with raises(AssertionError, match=f'size of file {huge_f.path} = 700.0B, while limit = 600.0B'):
        check_limits(get_cfg(inputs=[]), [huge_f.get_file()])
    with raises(AssertionError, match='total size of input files = 2.0KB, while limit = 2.0KB.'):
        check_limits(get_cfg(inputs=[big_path] * 4), [])
    with raises(AssertionError, match='total size of input files and Python local modules = 2.5KB, while limit = 2.0KB.'):
        check_limits(get_cfg(inputs=[big_path] * 2), [big_path.get_file()] * 3)

    with raises(AssertionError, match='number of input files must be not greater than 2'):
        check_limits(get_cfg(inputs=paths), [])
    with raises(AssertionError, match='number of output files must be not greater than 2'):
        check_limits(get_cfg(outputs=paths), [])
    with raises(AssertionError, match='number of s3 mounts must be not greater than 2'):
        check_limits(get_cfg(s3_mounts=paths), [])
    with raises(AssertionError, match='number of datasets must be not greater than 2'):
        check_limits(get_cfg(datasets=paths), [])
