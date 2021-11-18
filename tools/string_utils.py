import time
import string
import random
from re import sub

"""
Модуль преобразования строковых представлений
"""


def random_string(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def random_test_name(length=10, prefix=None):
    letters = string.ascii_lowercase
    result_prefix = prefix if prefix is not None else 'Test'
    return result_prefix + ''.join(random.choice(letters) for _ in range(length))


def random_email():
    return f'autotest{str(int(round(time.time() * 1000)))}@yopmail.com'


def random_id(length=10):
    digits = string.digits
    return 'id' + ''.join(random.choice(digits) for _ in range(length))


def regex_datetime(origin_time):
    return sub('.\(.*', "", origin_time)


def calculate_percentage_value(origin_value, percentage):
    result_value = float(origin_value) - (float(origin_value) * percentage / 100)
    return "%.2f" % result_value
