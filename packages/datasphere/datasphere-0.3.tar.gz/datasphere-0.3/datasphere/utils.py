import hashlib
from tabulate import tabulate
from typing import BinaryIO, List, Optional, Tuple

from google.protobuf.timestamp_pb2 import Timestamp

from yandex.cloud.datasphere.v2.jobs.jobs_pb2 import Job, _JOBSTATUS


def get_sha256_and_size(f: BinaryIO) -> Tuple[str, int]:
    h = hashlib.sha256()
    sz = 0

    for chunk in iter(lambda: f.read(65_536), b''):
        h.update(chunk)
        sz += len(chunk)

    return h.hexdigest(), sz


def format_jobs_table(jobs: List[Job]) -> str:
    def format_timestamp(ts: Optional[Timestamp]) -> str:
        if not ts or (ts.seconds == 0 and ts.nanos == 0):
            return ''
        return ts.ToDatetime().isoformat()

    def get_row(job: Job) -> list:
        return [
            job.id,
            job.name,
            job.desc,
            format_timestamp(job.created_at),
            format_timestamp(job.finished_at),
            _JOBSTATUS.values_by_number[job.status].name,
            job.created_by_id,
        ]

    return tabulate(
        [get_row(job) for job in jobs],
        headers=['ID', 'Name', 'Description', 'Created at', 'Finished at', 'Status', 'Created by'],
    )


def query_yes_no(question: str, default: Optional[bool] = True) -> bool:
    prompt = {True: 'Y/n', False: 'y/N', None: 'y/n'}[default]
    options = {'yes': True, 'y': True, 'no': False, 'n': False}
    while True:
        choice = input(f'{question} [{prompt}]: ').lower()
        if default is not None and choice == '':
            return default
        elif choice in options:
            return options[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').")


def humanize_bytes_size(size: int) -> str:
    for unit in ('', 'K', 'M', 'G', 'T', 'P', 'E', 'Z'):
        if abs(size) < 1024.0:
            return f'{size:3.1f}{unit}B'
        size /= 1024.0
    return f'{size:.1f}YB'
