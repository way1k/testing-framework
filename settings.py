import os.path
from pathlib import Path

PROJECT_DIR = str(Path(__file__).parent)
CONFIG_DIR = os.path.join(PROJECT_DIR, "config")
PLUGINS_DIR = os.path.join(PROJECT_DIR, "plugins")
ALLURE_FILES_DIR = os.path.join(PROJECT_DIR, "files/tmp/allure-results")
LOCAL_FILES_DIR = os.path.join(PROJECT_DIR, "files/tmp")
REMOTE_FILES_DIR = "/home/selenium/Downloads/"

TEST_PDF_FILE = os.path.join(PROJECT_DIR, "files/etc/pdf_document.pdf")
TEST_TXT_FILE = os.path.join(PROJECT_DIR, "files/etc/text_file.txt")

ALLURE_REPORT = {"results_dir": ALLURE_FILES_DIR, "url": "http://31.207.44.170:8081"}

SELENOID_ENDPOINT = "http://31.207.44.170:4444/wd/hub"
SELENOID_DOWNLOAD = "http://31.207.44.170:4444/download/"
