import logging
import os
import random
import re
import subprocess
import time
import uuid
from datetime import datetime
from pathlib import Path

import requests

from conf import PRJ_PATH, LOG_DIR, LOG_LEVEL
from conf import TWEET_ENDPOINT, COMMENT_ENDPOINT
from log import Log

_log_name = Path(__file__).stem if __name__ == '__main__' else __name__
if not LOG_DIR:
    _log_file = PRJ_PATH / (Path(__file__).stem + '.log')
else:
    _log_file = PRJ_PATH / LOG_DIR / (Path(__file__).stem + '.log')
LOGGER = Log(log_name=_log_name, log_level=LOG_LEVEL,
             log_file=_log_file).logger


def random_sleep(min_sleep_time=1, max_sleep_time=5):
    sleep_time = random.randint(min_sleep_time, max_sleep_time)
    LOGGER.debug(f'Random sleep: {sleep_time}')
    time.sleep(sleep_time)


def get_datetime_str(fmtstr='%Y%m%d-%H%M%S'):
    """Get string of the current time.

    e.g.::

        format: %Y%m%d-%H%M%S
        time example: 20210701-150101
    """

    return datetime.now().strftime(fmtstr)


def get_datetime_date_str(fmtstr='%Y%m%d'):
    return get_datetime_str(fmtstr)


def set_log(prj_path, file_obj, name_obj, log_level=logging.DEBUG,
            log_dir='', log_suffix='.log'):
    _log_name = Path(file_obj).stem if name_obj == '__main__' else name_obj
    if not log_dir:
        _log_file = prj_path / (Path(file_obj).stem + log_suffix)
    else:
        _log_file = prj_path / log_dir / (Path(file_obj).stem + log_suffix)
    logger = Log(log_name=_log_name, log_level=log_level,
                 log_file=_log_file).logger

    return logger


def check_text_present_page_source(driver, text, logger):
    if re.findall(text, driver.page_source, flags=re.IGNORECASE):
        logger.debug(f'Find the text in page source: "{text}"')
        return True
    else:
        logger.debug(f'Cannot find the text in page source: "{text}"')
        return False


def get_random_file_name(min_len=10, max_len=20, suffix=''):
    return ''.join(random.choices(uuid.uuid4().hex,
                                  k=random.randrange(min_len, max_len))) + suffix


def _add_suffix_name(fname, suffix='_small', repeate=False):
    fnames = fname.split('.')
    if len(fnames) == 1:
        if not repeate:
            return fname if fname.endswith(suffix) else (fname + suffix)
        else:
            return fname + suffix

    else:
        if not repeate:
            names = '.'.join(fnames[:-1])
            return fname if names.endswith(suffix) else (
                    names + suffix + '.' + fnames[-1])
        else:
            return '.'.join(fnames[:-1]) + suffix + '.' + fnames[-1]





def get_absolute_path_str(path):
    if isinstance(path, Path):
        absolute_path = str(path.absolute())
    elif isinstance(path, str):
        absolute_path = os.path.abspath(path)
    else:
        LOGGER.debug(f'Other type of path: {type(path)}')
        absolute_path = path

    #  LOGGER.debug(f'Absolute path: "{absolute_path}" from "{path}"')
    return absolute_path


def get_random_records(records, model, max_records=10):
    ids = [e.id for e in records]
    all_number = len(ids)
    max_select_number = min(max_records, all_number)
    select_number = random.randint(1, max_select_number)
    random_ids = random.choices(ids, k=select_number)
    return model.objects.filter(id__in=random_ids)

def run_cmd(cmd, verbose=True):
    """Run shell commands, and return the results

    ``cmd`` should be a string like typing it in shell.
    """
    try:
        if verbose:
            LOGGER.debug(f'Command: {cmd}')

        r = subprocess.run(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, shell=True, text=True)

        if verbose:
            if r.returncode == 0:
                LOGGER.debug(f'Successful to run the command: {cmd}')
                LOGGER.debug(f'Result of the command: {r.stdout}')
            else:
                LOGGER.warning(f'Failed to run the command: {cmd}')
                LOGGER.debug(f'Result of the command: {r.stdout}')

        return r.returncode, r.stdout
    except Exception as e:
        LOGGER.error(e)


def run_cmd_without_exit(cmd, verbose=True, shell=False):
    """Run shell commands, and return the results

    ``cmd`` should be a string like typing it in shell.
    """
    try:
        if verbose:
            LOGGER.debug(f'Command: {cmd}')

        process = subprocess.Popen(cmd, shell=shell)
        return process
    except Exception as e:
        LOGGER.error(e)


def run_cmd_loop(cmd, success_code=0, retry_times=3, sleep_time=2,
                 verbose=True):
    """Run the command until beyond the retry times or successfully"""
    times = 0
    while times <= retry_times:
        result = run_cmd(cmd, verbose=verbose)
        if result:
            (status, output) = result
        else:
            times += 1
            if sleep_time > 0:
                time.sleep(sleep_time)
            LOGGER.debug(f'Retry to run the command: {cmd}')
            continue

        if status == success_code:
            return True
        else:
            times += 1
            if sleep_time > 0:
                time.sleep(sleep_time)
            LOGGER.debug(f'Retry to run the command: {cmd}')
            continue

    return False


def kill_process_after_waiting(pid, success_code=0, retry_times=3,
                               sleep_time=2, verbose=True):
    """Using process ID to kill a process"""
    # if the process exits normally, then kill it forcely
    search_pid_cmd = f'ps --pid {pid}'
    if not run_cmd_loop(search_pid_cmd, success_code=success_code,
                        verbose=verbose):
        kill_cmd = f'kill -9 {pid}'
        LOGGER.debug(f'Kill the process forcely: {pid}')
        run_cmd(kill_cmd, verbose=verbose)


def pkill_process_after_waiting(pname, success_code=0, retry_times=3,
                                sleep_time=2, verbose=True):
    """Using process name to kill a process"""
    # if the process exits normally, then kill it forcely
    search_pid_cmd = f'pgrep {pname}'
    if not run_cmd_loop(search_pid_cmd, success_code=success_code,
                        verbose=verbose):
        kill_cmd = f'pkill -9 {pname}'
        LOGGER.debug(f'Kill the process forcely: {pname}')
        run_cmd(kill_cmd, verbose=verbose)


def get_listening_pid(host, port):
    cmd = f'lsof -i tcp@{host}:{port} -sTCP:LISTEN -t'
    result = run_cmd(cmd)
    if result:
        (returncode, output) = result
        if output:
            # output is the pid
            return output
    return ''


def get_commands_by_pattern(pattern, verbose=False):
    #  cmd = f'pgrep -f {pattern}'
    cmd = f'pgrep -a -f {pattern}'
    result = run_cmd(cmd)

    if verbose:
        LOGGER.debug(f'Result: {result}')

    if result:
        (returncode, output) = result
        if output:
            # output is the pid
            return tuple(e for e in output.strip().split('\n'))
    return tuple()


def get_installed_packages():
    cmd = 'sdkmanager --list_installed'
    result = run_cmd(cmd, False)
    if result:
        (returncode, output) = result
        if output:
            return output
    return ''
