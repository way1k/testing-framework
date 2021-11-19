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

ALLURE_REPORT = {
    "results_dir": ALLURE_FILES_DIR,
    "url": "http://132.226.129.89:8081"
}

SELENOID_ENDPOINT = "http://143.47.227.244:4444/wd/hub"
SELENOID_DOWNLOAD = "http://143.47.227.244:4444/download/"

# SELENOID_GGR_HOST = "10.31.85.146:4444"
# SELENOID_GGR_USER = "pytest_framework"
# SELENOID_GGR_PASSWORD = "pytest_framework_password_123"
# SELENOID_GGR_ENDPOINT = f"http://{SELENOID_GGR_USER}:{SELENOID_GGR_PASSWORD}@{SELENOID_GGR_HOST}/wd/hub"
# SELENOID_GGR_DOWNLOAD = f"http://{SELENOID_GGR_USER}:{SELENOID_GGR_PASSWORD}@{SELENOID_GGR_HOST}/download/"
