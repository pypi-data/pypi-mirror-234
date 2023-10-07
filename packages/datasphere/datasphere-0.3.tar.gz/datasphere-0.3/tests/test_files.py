import hashlib
import logging
from unittest.mock import Mock
import requests
from typing import BinaryIO

from yandex.cloud.datasphere.v2.jobs.jobs_pb2 import StorageFile, File, FileDesc

from datasphere.files import prepare_local_modules, upload_files, download_files
from datasphere.pyenv import PythonEnv


def test_prepare_local_modules(tmp_path, mocker):
    py_env = PythonEnv(
        python_version='',
        local_modules_paths=['main.py', 'lib/'],
        pypi_packages={},
    )

    # mock archive with file with module name as content
    def zip_path(module: str, ar: BinaryIO):
        with open(ar.name, 'w') as ar_w:
            ar_w.write(module)
            ar_w.seek(0)

    mocker.patch('datasphere.files.zip_path', zip_path)

    paths = prepare_local_modules(py_env, str(tmp_path))

    for path, expected_var, expected_hash in (
            (paths[0], '_LOCAL_MODULE_0', hashlib.sha256(b'main.py').hexdigest()),
            (paths[1], '_LOCAL_MODULE_1', hashlib.sha256(b'lib/').hexdigest())
    ):
        assert path.path.startswith(str(tmp_path))
        assert path.var == expected_var
        f = path.get_file()
        assert f.desc.path == path.path
        assert f.desc.var == expected_var
        assert f.sha256 == expected_hash


def test_upload_files(tmp_path, mocker, caplog):
    file_1 = tmp_path / '1.txt'
    file_2 = tmp_path / '2.txt'

    file_1.write_text('qwerty')
    file_2.write_text('foo')

    files = [
        StorageFile(
            file=File(
                desc=FileDesc(path=str(file_1.absolute())),
                sha256='file1_sha256',
            ),
            url='https://storage.net/my-bucket/my-key-1',
        ),
        StorageFile(
            file=File(
                desc=FileDesc(path=str(file_2.absolute())),
                sha256='file2_sha256',
            ),
            url='https://storage.net/my-bucket/my-key-2',
        ),
    ]

    sha256_to_display_path = {'file2_sha256': 'pretty_path.txt'}

    contents = []

    # Let upload content be file content along with url
    def put(url: str, data: BinaryIO):
        contents.append(url.encode('utf8') + b' ' + data.read())
        return Mock(status_code=200)

    mocker.patch('requests.put', put)

    caplog.set_level(logging.DEBUG)

    upload_files(files, sha256_to_display_path)

    assert contents == [
        b'https://storage.net/my-bucket/my-key-1 qwerty',
        b'https://storage.net/my-bucket/my-key-2 foo',
    ]
    assert caplog.record_tuples == [
        ('datasphere.files', 20, 'uploading 2 files (0.0B) ...'),
        ('datasphere.files', 10, f'uploading file `{tmp_path}/1.txt` (0.0B) ...'),
        ('datasphere.files', 10, 'uploading file `pretty_path.txt` (0.0B) ...'),
        ('datasphere.files', 20, 'files are uploaded'),
    ]


def test_download_files(tmp_path, mocker, caplog):
    file_1 = tmp_path / '1.txt'
    file_2 = tmp_path / 'dir' / 'subdir' / '2.txt'  # Sub dirs will be created automatically.

    # File which we download will contain url as first line, then offset of chunk.
    def get(url: str) -> requests.Response:
        resp = Mock(status_code=200)

        def iter_content(chunk_size: int):
            yield url.encode('utf8') + b' '
            for i in range(0, (1 << 24) + 10, chunk_size):
                # No need to return chunk_size length byte string, let's return just offset.
                yield bytes(str(i), encoding='utf8') + b' '

        resp.iter_content = iter_content
        return resp

    mocker.patch('requests.get', get)

    files = [
        StorageFile(
            file=File(
                desc=FileDesc(path=str(path.absolute())),
                sha256=b'',  # not important
            ),
            url=url,
        )
        for path, url in zip(
            (file_1, file_2),
            ('https://storage.net/my-bucket/my-key-1', 'https://storage.net/my-bucket/my-key-2')
        )
    ]

    caplog.set_level(logging.DEBUG)

    download_files(files)

    assert file_1.read_text() == 'https://storage.net/my-bucket/my-key-1 0 16777216 '
    assert file_2.read_text() == 'https://storage.net/my-bucket/my-key-2 0 16777216 '

    assert caplog.record_tuples == [
        ('datasphere.files', 20, 'downloading 2 files (0.0B) ...'),
        ('datasphere.files', 10, f'downloading file `{tmp_path}/1.txt` (0.0B) ...'),
        ('datasphere.files', 10, f'downloading file `{tmp_path}/dir/subdir/2.txt` (0.0B) ...'),
        ('datasphere.files', 20, 'files are downloaded'),
    ]
