import string
import random
from datetime import datetime, timedelta

"""
Модуль генерации случайных данных
"""


def random_string(length):
    """
    Создает строку из случайных символов в заданном диапазоне
    :param length: диапазон
    :return: string
    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(1, length))


def random_uppercase_string(length):
    """
    Создает строку с верхним регистром заданной длинны
    :param length: длинна строки
    :return: string
    """
    letters = 'ABCDEF0123456789'
    return ''.join(random.choices(letters.upper(), k=length))


def random_digits_in_range(start, end):
    """
    Создает случайное число в заданном диапазоне
    :param start:
    :param end:
    :return:
    """
    return random.randrange(start, end)


def constant_length_random_number(length):
    """
    Создает случайное числовое значение заданной длинны
    :param length:
    :return: string
    """
    return int(''.join(random.choices(string.digits, k=length)))


def generate_timestamp(days):
    """
    Создает строку временем и датой в будущем
    :param days:
    :return: int
    """
    return int(datetime.timestamp(datetime.now() + timedelta(days=days)))


def generate_date_in_future(date_format: str, days: int = 0, hours: int = 0, minutes: int = 0):
    """
    Создает строку временем и датой в будущем по указанному формату
    :param hours:
    :param days:
    :param minutes:
    :param date_format:
    :return: datetime string
    """
    return datetime.strftime(datetime.now() + timedelta(days=days, hours=hours, minutes=minutes), date_format)


def generate_now_date(date_format):
    """
    Создает строку с текущим временем и датой
    :param date_format:
    :return: datetime string
    """
    return datetime.strftime(datetime.now(), date_format)


def generate_date_in_past(date_format: str, days: int = 0, hours: int = 0, minutes: int = 0):
    """
    Создает строку временем и датой в прошлом по указанному формату
    :param hours:
    :param minutes:
    :param days:
    :param date_format:
    :return: datetime string
    """
    return datetime.strftime(datetime.now() - timedelta(days=days, hours=hours, minutes=minutes), date_format)
