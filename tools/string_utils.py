import random
import string
import time


def random_string(length=5):
    """Generates a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def random_test_name(length=10, prefix=None):
    """Generates random name"""
    letters = string.ascii_lowercase
    result_prefix = prefix if prefix is not None else 'Test'
    return result_prefix + ''.join(random.choice(letters) for _ in range(length))


def random_email():
    """Generates user email for tests"""
    return f'autotest{str(int(round(time.time() * 1000)))}@yopmail.com'


def random_id(length=10):
    """Generates random user social ID"""
    digits = string.digits
    return 'id' + ''.join(random.choice(digits) for _ in range(length))
