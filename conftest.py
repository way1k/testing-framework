from fixtures.app import *
from fixtures.common import *


def pytest_addoption(parser):

    parser.addoption(
        "--config",
        action="store",
        help="Test stand number",
        default="config_test_instagram"
    )

    parser.addoption(
        "--browser",
        action="store",
        help="Select browser",
        default="chrome",
    )
