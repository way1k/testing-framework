import logging
import os
import json
import shutil
from lxml import etree
from random import randrange
from settings import LOCAL_FILES_DIR

"""
Модуль работы с файлами
"""


def create_file_with_random_size(file_min_size=1, file_max_size=10, file_type='txt', file_name='generated_file'):
    with open(os.path.join(os.path.join(LOCAL_FILES_DIR), f'{file_name}.{file_type}'), mode='w') as f:
        generate_file_size = randrange(file_min_size*(1024*1024), file_max_size*(1024*1024))
        f.seek(generate_file_size-1)
        f.write("\0")
        f.close()
    logging.info(f"Сгенерирован файл '{file_name}.{file_type}' размером '{generate_file_size//(1024*1024)}' Мбайт")


def copy_test_files(files_directory):
    files_in_directory = [
        files for files in os.listdir(files_directory) if os.path.isfile(os.path.join(files_directory, files))
    ]
    for file in files_in_directory:
        copied_file_name = "copy_" + file
        source_file = os.path.join(f"{files_directory}", file)
        copied_file = os.path.join(f"{files_directory}", copied_file_name)
        shutil.copyfile(source_file, copied_file)


def clean_copied_test_files(files_directory):
    for copied_files in os.listdir(f"{files_directory}"):
        if copied_files.startswith("copy_"):
            os.remove(os.path.join(files_directory, copied_files))


def load_file(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', file), encoding="utf-8") as f:
        file_info = json.load(f)
    return file_info


def parse_xml(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', file), encoding="utf-8") as f:
        file_info = etree.parse(f)
    return file_info


def read_file(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', file), encoding="utf-8") as f:
        file_info = f.read()
    return file_info


def write_to_file(file, new_record):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', file), encoding="utf-8") as f:
        _ = f.write(new_record)
    return _
