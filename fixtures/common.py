import pytest
import configparser
from tools.path_utils import get_root_dir


@pytest.fixture(scope="session")
def cfg(request):
    """Fixture for work with config.ini"""
    cfg = configparser.ConfigParser()
    cfg_file_path = f"{get_root_dir()}/config/{request.config.getoption('--config')}.ini"
    cfg.read(cfg_file_path)
    yield cfg
