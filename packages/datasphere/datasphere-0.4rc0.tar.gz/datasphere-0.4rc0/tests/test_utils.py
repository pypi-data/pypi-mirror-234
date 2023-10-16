from datasphere.utils import format_jobs_table, query_yes_no, humanize_bytes_size
from datetime import datetime, timezone

from google.protobuf.timestamp_pb2 import Timestamp

from yandex.cloud.datasphere.v2.jobs.jobs_pb2 import Job, JobStatus


def test_format_jobs_table():
    def get_ts(dt: datetime) -> Timestamp:
        ts = Timestamp()
        ts.FromDatetime(dt)
        return ts

    jobs = [
        Job(
            id='bt12tlsc3nkt2opg2h61',
            name='my script',
            desc='This script is doing cool ML stuff',
            created_at=get_ts(datetime(year=2022, month=4, day=15, tzinfo=timezone.utc)),
            finished_at=get_ts(datetime(year=2022, month=4, day=16, tzinfo=timezone.utc)),
            status=JobStatus.SUCCESS,
            created_by_id='Bob',
        ),
        Job(
            id='bt10gr4c1b081bidoses',
            created_at=get_ts(datetime(year=2022, month=5, day=2, tzinfo=timezone.utc)),
            status=JobStatus.EXECUTING,
            created_by_id='Alice',
        )
    ]
    assert format_jobs_table(jobs) == """
ID                    Name       Description                         Created at           Finished at          Status     Created by
--------------------  ---------  ----------------------------------  -------------------  -------------------  ---------  ------------
bt12tlsc3nkt2opg2h61  my script  This script is doing cool ML stuff  2022-04-15T00:00:00  2022-04-16T00:00:00  SUCCESS    Bob
bt10gr4c1b081bidoses                                                 2022-05-02T00:00:00                       EXECUTING  Alice
    """.strip()


def test_query_yes_no(mocker):
    for choice, default, expected in (
            ('', True, True),
            ('y', True, True),
            ('N', True, False),
            ('Yes', False, True),
            ('', False, False),
            ('no', False, False),
    ):
        mocker.patch('datasphere.utils.input', lambda _: choice)
        assert query_yes_no('do stuff?', default=default) is expected


def test_humanize_bytes_size():
    for size, expected in (
            (1, '1.0B'),
            (900, '900.0B'),
            (2500, '2.4KB'),
            (1 << 20, '1.0MB'),
            (10 * (1 << 30), '10.0GB'),
    ):
        assert humanize_bytes_size(size) == expected
