import os
import shutil
import pathlib
import zipfile
from logging import info as ilog
from settings import PROJECT_DIR


def get_active_branch_name():
    head_dir = PROJECT_DIR + "/.git/HEAD"
    with open(head_dir, "r") as f:
        content = f.read().splitlines()
    for line in content:
        if line[0:4] == "ref:":
            return line.partition("refs/heads/")[2]


def get_platform(config):
    if config.getoption('browser') == 'local':
        platform = f'local/chrome'
    else:
        platform = f'remote/{config.getoption("browser")}'
    return platform


def print_(text, *args, **kwargs):
    text_color = "\033[94m"
    end = '\033[0m'
    ilog(text_color + text + end, *args, **kwargs)


def compress_to_zip(folder, zip_name):
    files = [file for _, _, file in os.walk(folder)][0]
    with zipfile.ZipFile(zip_name, "w") as zipf:
        for file in files:
            zipf.write(
                filename=str(pathlib.PurePath(folder, file)),
                arcname=os.path.basename(file),
                compress_type=zipfile.ZIP_DEFLATED
            )


def cleanup(*items):
    for item in items:
        if os.path.isfile(item):
            os.remove(item)
        elif os.path.isdir(item):
            shutil.rmtree(item, ignore_errors=True)
