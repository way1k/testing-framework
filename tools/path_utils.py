import os


def get_root_dir():
    """Gets string representation of project directory"""
    return str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
