"""
"""
import os
import sys
import time
import shutil
import subprocess


def print_progress(count, total):
    '''
    Print a progress in the terminal
    :param count:
    :param total:
    :return:
    '''
    # Percentage completion.
    pct_complete = float(count) / total

    # Status-message.
    # Note the \r which means the line should overwrite itself.
    msg = "\r- Progress: {0:.1%}".format(pct_complete)

    # Print it.
    sys.stdout.write(msg)
    sys.stdout.flush()


def find_files(directory, pattern=['.wav']):
    '''
    Recursively finds all files matching the pattern
    :param directory: Path to a directory with files
    :param pattern: extension of the files
    :return: Generator via files
    '''
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if len(pattern):
                for exten in pattern:
                    if filename.endswith(exten):
                        yield os.path.join(root, filename)
            else:
                yield os.path.join(root, filename)


def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def remove_dir(dir_path):
    if os.path.exists(dir_path):
        try:
            shutil.rmtree(dir_path)
        except OSError as e:
            print("Error: %s : %s" % (dir_path, e.strerror))


def remove_file(file_path):
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
        except OSError as e:
            print("Error: %s : %s" % (file_path, e.strerror))


def clock():
    try:
        return time.perf_counter()  # Python 3
    except:
        return time.clock()  # Python 2


class Timer:
    def __init__(self, granularity='s'):
        """
        :param granularity: can be s - seconds, m - minutes, h - hours
        :return:
        """
        self.granularity = granularity

    # Begin of `with` block
    def __enter__(self):
        if self.granularity == 'm':
            self.start_time = clock() / 60
        elif self.granularity == 'h':
            self.start_time = (clock() / 60) / 60
        else:
            self.start_time = clock()
        self.end_time = None

        return self

    # End of `with` block
    def __exit__(self, exc_type, exc_value, tb):
        if self.granularity == 'm':
            self.end_time = clock() / 60
        elif self.granularity == 'h':
            self.end_time = (clock() / 60) / 60
        else:
            self.end_time = clock()

    def elapsed_time(self):
        """Return elapsed time in seconds"""
        if self.end_time is None:
            # still running
            return clock() - self.start_time
        else:
            return self.end_time - self.start_time


def run_cmd(args_list: [list, str], env: dict = None, shell: bool = False):
    """
    Run linux commands.
    """
    # import subprocess
    print('Running system command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, env=env, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_output, s_err = proc.communicate()
    s_return = proc.returncode

    return s_return, s_output, s_err
