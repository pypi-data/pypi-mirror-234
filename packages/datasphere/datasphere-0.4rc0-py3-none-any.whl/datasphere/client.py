import logging
from threading import Thread
from time import sleep
from typing import Dict, List, Optional, Tuple

from google.rpc.code_pb2 import _CODE
import grpc
from yandex.cloud.datasphere.v2.jobs.jobs_pb2 import JobParameters, Job
from yandex.cloud.datasphere.v2.jobs.project_job_service_pb2 import (
    CreateProjectJobRequest, CreateProjectJobResponse,
    ExecuteProjectJobRequest, ExecuteProjectJobResponse, ExecuteProjectJobMetadata,
    ReadProjectJobStdLogsRequest, StdLog,
    ListProjectJobRequest, GetProjectJobRequest, DeleteProjectJobRequest,
    CancelProjectJobRequest,
)
from yandex.cloud.datasphere.v2.jobs.project_job_service_pb2_grpc import ProjectJobServiceStub
from yandex.cloud.datasphere.v2.project_service_pb2_grpc import ProjectServiceStub
from yandex.cloud.datasphere.v2.project_service_pb2 import GetProjectRequest
from yandex.cloud.operation.operation_pb2 import Operation
from yandex.cloud.operation.operation_service_pb2 import GetOperationRequest
from yandex.cloud.operation.operation_service_pb2_grpc import OperationServiceStub

from datasphere.auth import get_md
from datasphere.channel import get_channels
from datasphere.config import Config
from datasphere.files import download_files, upload_files
from datasphere.logs import system_stdout, system_stderr, program_stdout, program_stderr
from datasphere.utils import query_yes_no

logger = logging.getLogger(__name__)

operation_check_interval_seconds = 5
log_read_interval_seconds = 5

system_log_prefix = '[SYS] '
loggers_map = {  # (log type, is system) -> logger
    (StdLog.Type.OUT, True): system_stdout,
    (StdLog.Type.ERR, True): system_stderr,
    (StdLog.Type.OUT, False): program_stdout,
    (StdLog.Type.ERR, False): program_stderr,
}


class Client:
    cfg: Config
    md: List[Tuple[str, str]]

    stub: ProjectJobServiceStub
    prj_stub: ProjectServiceStub
    op_stub: OperationServiceStub

    def __init__(self, oauth_token: Optional[str] = None):
        self.md = get_md(oauth_token)
        chan, op_chan = get_channels()
        self.stub = ProjectJobServiceStub(chan)
        # self.prj_stub = ProjectServiceStub(chan)
        self.op_stub = OperationServiceStub(op_chan)

    def create(
            self,
            job_params: JobParameters,
            cfg: Config,
            project_id: str,
            sha256_to_display_path: Dict[str, str],
    ) -> str:
        logger.info('creating job ...')
        op, create_call = self.stub.Create.with_call(
            CreateProjectJobRequest(
                project_id=project_id,
                job_parameters=job_params,
                config=cfg.content,
                name=cfg.name,
                desc=cfg.desc,
            ),
            metadata=self.md,
        )
        op = self._poll_operation(op, create_call)
        resp = CreateProjectJobResponse()
        op.response.Unpack(resp)
        upload_files(list(resp.upload_files), sha256_to_display_path)
        logger.info('created job `%s`', resp.job_id)
        return resp.job_id

    def execute(self, job_id: str, std_logs_offset: int = 0) -> Tuple[Operation, grpc.Call]:
        self.read_std_logs(job_id, std_logs_offset)
        logger.debug('executing job ...')
        return self.stub.Execute.with_call(ExecuteProjectJobRequest(job_id=job_id), metadata=self.md)

    def list(self, project_id: str) -> List[Job]:
        page_token = None
        jobs = []
        while True:
            resp = self.stub.List(
                ListProjectJobRequest(project_id=project_id, page_size=50, page_token=page_token),
                metadata=self.md,
            )
            jobs += resp.jobs
            page_token = resp.page_token
            if not page_token or len(resp.jobs) == 0:
                break
        return jobs

    def get(self, job_id: str) -> Job:
        return self.stub.Get(GetProjectJobRequest(job_id=job_id), metadata=self.md)

    def delete(self, job_id: str):
        self.stub.Delete(DeleteProjectJobRequest(job_id=job_id), metadata=self.md)

    def wait_for_completion(self, op: Operation, call_which_created_op: grpc.Call):
        logger.info('executing job ...')
        try:
            op = self._poll_operation(op, call_which_created_op)
        finally:
            # TODO: currently op_meta.job.project_id is empty, waiting for server-side fix
            pass
            # op_meta = ExecuteProjectJobMetadata()
            # op.metadata.Unpack(op_meta)
            # self._display_job_link(op_meta.job)
        resp = ExecuteProjectJobResponse()
        op.response.Unpack(resp)
        download_files(list(resp.output_files))
        if resp.result.return_code != 0:
            raise ProgramError(resp.result.return_code)
        logger.info('job completed successfully')

    # Wait until operation is done, if it's error in operation, raise it as in case of usual gRPC call.
    def _poll_operation(self, op: Operation, call_which_created_op: grpc.Call) -> Operation:
        while True:
            try:
                if not op.done:
                    logger.debug('waiting for operation ...')
                    sleep(operation_check_interval_seconds)
                else:
                    if op.HasField('error'):
                        raise OperationError(op, call_which_created_op)
                    else:
                        # We are ready to unpack response.
                        return op
                op = self.op_stub.Get(GetOperationRequest(operation_id=op.id), metadata=self.md)
            except KeyboardInterrupt:
                if query_yes_no('cancel job?', default=False):
                    logger.info('cancelling job ...')
                    op_meta = ExecuteProjectJobMetadata()
                    op.metadata.Unpack(op_meta)
                    self.stub.Cancel(CancelProjectJobRequest(job_id=op_meta.job.id), metadata=self.md)
                    logger.info('job is canceled')
                    raise
                else:
                    logger.info('resuming job')

    def read_std_logs(self, job_id: str, offset: int):
        Thread(target=self._print_std_logs, args=[job_id, offset], daemon=True).start()

    def _print_std_logs(self, job_id: str, offset: int):
        # Server has two possible ways to return streaming response with logs:
        # 1) Stream will end only after job finish.
        # 2) Stream can end at any moment, and we have to make several requests remembering last offset.
        #
        # We don't know which way server will use, so we support both ways. Because of 1), we can read logs only
        # in separate thread. Because of 2), we remember offset and make requests in infinite loop, which will
        # terminate with daemon thread termination.
        #
        # In case of attach to executing job, we send offset = -1 to indicate that we want to get logs from current
        # moment at time.
        #
        # Opened questions:
        # - Logs read will end after downloading results (CLI process finish), some final logs may be lost.

        while True:
            try:
                for resp in self.stub.ReadStdLogs(ReadProjectJobStdLogsRequest(
                        job_id=job_id, offset=offset), metadata=self.md):
                    for log in resp.logs:
                        try:
                            lines = log.content.decode('utf8').strip().split('\n')
                        except UnicodeError:
                            lines = [f'[non-utf8 sequence] {log.content}']

                        for line in lines:
                            if not line:
                                # Server sometimes sends empty logs.
                                continue
                            # In future server will send separate `boolean system` flag in each message.
                            system = False
                            if line.startswith(system_log_prefix):
                                system = True
                                line = line[len(system_log_prefix):]
                            job_logger = loggers_map.get((log.type, system))
                            if job_logger:
                                job_logger.info(line)
                    offset = resp.offset
            except grpc.RpcError as e:
                # Sometimes stream interrupts, it's ok, and we create new one from current offset.
                is_stream_interruption = (
                        e.code() == grpc.StatusCode.UNAVAILABLE and
                        e.details().startswith('stream timeout')
                        or
                        e.code() == grpc.StatusCode.INTERNAL and
                        e.details().startswith('Received RST_STREAM')
                )
                if not is_stream_interruption:
                    raise
                logger.debug('read std logs stream interrupted, creating new one from offset %d', offset)
            sleep(log_read_interval_seconds)

    def _display_job_link(self, job: Job):
        project_id = job.project_id
        try:
            community_id = self._get_community_id(project_id)
        except grpc.RpcError as e:
            # Job link is nice to have, but if we couldn't get community info,
            # lets just log the error and do not crush the process.
            logger.warning('Failed to get community ID by project ID for job link generation')
            logger.exception(e)
            return
        # TODO: .ru TLD is hard-coded
        link = f'https://datasphere.yandex.ru/communities/{community_id}/projects/{project_id}/job/{job.id}'
        logger.info('job link: %s', link)

    def _get_community_id(self, project_id: str) -> str:
        return self.prj_stub.Get(GetProjectRequest(project_id=project_id), metadata=self.md).community_id


# Exception to display traceback about operation errors in similar way as usual RPC error (grpc.RpcError).
class OperationError(Exception):
    def __init__(self, op: Operation, call_which_created_op: grpc.Call):
        self.op = op
        self.call_which_created_op = call_which_created_op

    def __str__(self):
        status = self.op.error
        code = _CODE.values_by_number[status.code].name
        return f'Operation returned error:\n\tstatus={code}\n\tdetails={status.message}'

    def __repr__(self):
        return str(type(self))


class ProgramError(Exception):
    def __init__(self, return_code: int):
        self.return_code = return_code

    def __str__(self):
        return f'Program returned code {self.return_code}'

    def __repr__(self):
        return str(type(self))
