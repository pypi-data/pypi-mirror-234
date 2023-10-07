import argparse
import grpc
import logging
import tempfile

from datasphere.client import Client, OperationError, ProgramError
from datasphere.config import parse_config, check_limits
from datasphere.files import prepare_local_modules
from datasphere.logs import configure_logging
from datasphere.pyenv import get_auto_py_env
from datasphere.utils import format_jobs_table

logger = logging.getLogger('datasphere.main')
# logger for things which do not go through logging, such as traceback in stderr
logger_file = logging.getLogger('datasphere_file')


def execute(args):
    cfg = parse_config(args.config)

    py_env = None
    if cfg.python_script:
        # If user didn't specify manual Python environment in config, we take Python interpreter version the same as
        # interpreter running this CLI program.
        logger.debug('exploring python env ...')
        py_env = get_auto_py_env(cfg.python_script)
        logger.debug('explored python env: %s', py_env)

    with tempfile.TemporaryDirectory(prefix='datasphere_') as tmpdir:
        logger.debug('using tmp dir `%s` to prepare local files', tmpdir)

        if py_env:
            local_modules = [f.get_file() for f in prepare_local_modules(py_env, tmpdir)]
            # Preserve original local modules paths (before archiving).
            sha256_to_display_path = {f.sha256: p for f, p in zip(local_modules, py_env.local_modules_paths)}
        else:
            local_modules = []
            sha256_to_display_path = {}

        check_limits(cfg, local_modules)

        job_params = cfg.get_job_params(py_env, local_modules)

        client = Client(args.token)

        job_id = client.create(job_params, cfg, args.project_id, sha256_to_display_path)
        op, execute_call = client.execute(job_id)
        logger.debug('operation `%s` executes the job', op.id)

    client.wait_for_completion(op, execute_call)


def attach(args):
    client = Client(args.token)
    # TODO: handle case of completed job, display DS job link with results.
    op, execute_call = client.execute(args.id, std_logs_offset=-1)
    client.wait_for_completion(op, execute_call)


def ls(args):
    client = Client(args.token)
    jobs = client.list(args.project_id)
    print(format_jobs_table(jobs))


def get(args):
    client = Client(args.token)
    job = client.get(args.id)
    print(format_jobs_table([job]))


def delete(args):
    client = Client(args.token)
    client.delete(args.id)
    logger.info('job deleted')


def build_arg_parser() -> argparse.ArgumentParser:
    parser_datasphere = argparse.ArgumentParser(prog='datasphere')
    parser_datasphere.add_argument(
        '-t', '--token', required=False,
        help='YC OAuth token, see https://cloud.yandex.com/docs/iam/concepts/authorization/oauth-token'
    )
    parser_datasphere.add_argument(
        '-l', '--log-level', required=False, default=logging.INFO,
        choices=[logging.getLevelName(level) for level in (logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG)],
        help='Logging level',
    )
    parser_datasphere.add_argument(
        '--log-config', required=False, type=argparse.FileType('r'), help='Custom logging config'
    )
    subparsers_datasphere = parser_datasphere.add_subparsers(required=True)

    parser_project = subparsers_datasphere.add_parser('project')
    subparsers_project = parser_project.add_subparsers(required=True)

    parser_job = subparsers_project.add_parser('job')
    subparsers_job = parser_job.add_subparsers(required=True)

    def add_project_id_argument(parser):
        parser.add_argument('-p', '--project-id', required=True, help='DataSphere project ID')

    def add_job_id_argument(parser):
        parser.add_argument('--id', required=True, help='Job ID')

    parser_execute = subparsers_job.add_parser('execute', help='Execute job')
    add_project_id_argument(parser_execute)
    parser_execute.add_argument('-c', '--config', required=True, help='Config file', type=argparse.FileType('r'))
    parser_execute.set_defaults(func=execute)

    parser_attach = subparsers_job.add_parser('attach', help='Attach to the job execution')
    add_job_id_argument(parser_attach)
    parser_attach.set_defaults(func=attach)

    parser_list = subparsers_job.add_parser('list', help='List jobs')
    add_project_id_argument(parser_list)
    parser_list.set_defaults(func=ls)

    parser_get = subparsers_job.add_parser('get', help='Get job')
    add_job_id_argument(parser_get)
    parser_get.set_defaults(func=get)

    parser_delete = subparsers_job.add_parser('delete', help='Delete job')
    add_job_id_argument(parser_delete)
    parser_delete.set_defaults(func=delete)

    return parser_datasphere


def main():
    arg_parser = build_arg_parser()

    args = arg_parser.parse_args()

    log_file_path = configure_logging(args.log_level, args.log_config)
    logger.info('log file path: %s', log_file_path)

    try:
        args.func(args)
    except Exception as e:
        log_exception(e, log_file_path)
        raise e


def log_exception(e: Exception, log_file_path: str):
    title = 'Error occurred'
    md = None
    if isinstance(e, grpc.RpcError):
        md = e.args[0].initial_metadata
        title = 'RPC error occurred'
    elif isinstance(e, OperationError):
        md = e.call_which_created_op.initial_metadata()
        title = 'Operation error occurred'
    elif isinstance(e, ProgramError):
        title = 'Program error occurred'
    md_str = '\n\theaders\n' + '\n'.join(f'\t\t{h.key}: {h.value}' for h in md) if md else ''
    logger.error('%s\n\tlog file path: %s%s', title, log_file_path, md_str)
    logger_file.exception(e)


if __name__ == '__main__':
    main()
