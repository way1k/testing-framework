import random
import string

from tools.time_utils import current_timestamp


def random_choice_from_sequence(sequence: list | tuple) -> any:
    """Generates a random choice from sequence"""
    return random.choice(sequence)


def random_string(length: int = 10) -> str:
    """Generates a random string of fixed length"""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def random_number(length: int = 10) -> str:
    """Generates a random string with digits of fixed length"""
    return "".join(random.choice(string.digits) for _ in range(length))


def random_digit_in_range(start: int, end: int) -> int:
    """
    Generates random number in a given range
    """
    return random.randrange(start, end)


def random_name(length: int = 10, prefix: str | None = None) -> str:
    """Generates random test user name"""
    letters = string.ascii_lowercase
    result_prefix = prefix if prefix is not None else "clain"
    return result_prefix + "".join(random.choice(letters) for _ in range(length))


def random_email() -> str:
    """Generates user email for tests"""
    return f"way1k_autotests{str(current_timestamp())}@gmail.com"


def random_password() -> str:
    """Generates password for tests"""
    return random_string(5).capitalize() + str(random_number())


def random_social_id() -> str:
    """Generates random user social ID"""
    return "id" + "".join(random.choice(string.digits) for _ in range(15))
