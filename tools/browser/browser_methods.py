import re
import glob
import allure
import requests
from time import sleep
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from tools.locator import Locator
from settings import REMOTE_FILES_DIR, LOCAL_FILES_DIR, SELENOID_DOWNLOAD


class BrowserMethods(BasePage):
    """
    Класс c описанием методов объекта браузера
    """

    """
    Методы прокрутки страницы
    """

    def scroll_to_top(self):
        self.browser.wd.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

    """
    Методы вкладок
    """

    def open_new_tab(self, link=''):
        self.browser.wd.execute_script(f"window.open('{link}','_blank')")

    def close_last_tab(self, back_to_tab: int = 0):
        if len(self.browser.wd.window_handles) > 1:
            self.browser.wd.switch_to.window(window_name=self.browser.wd.window_handles[-1])
            self.browser.wd.close()
            self.browser.wd.switch_to.window(window_name=self.browser.wd.window_handles[back_to_tab])

    def switch_to_new_tab(self):
        if len(self.browser.wd.window_handles) > 1:
            self.browser.wd.switch_to.window(window_name=self.browser.wd.window_handles[-1])

    def back_in_history_by_step(self, quantity_steps: int = 1):
        for step in range(quantity_steps):
            self.browser.wd.back()
        self.wait_for_ready_state_complete()

    """
    Общие методы
    """

    def get_session_id(self):
        return str(self.browser.wd.session_id)

    def screenshots(self, name='screenshot'):
        allure.attach(self.browser.wd.get_screenshot_as_png(), name=name, attachment_type=allure.attachment_type.PNG)

    """
    Методы загрузки файлов
    """

    def wait_for_download(self, timeout=30):
        sleep(2)
        seconds = 0
        download_timer = True
        while download_timer and seconds < timeout:
            sleep(1)
            download_timer = False
            for file_name in glob.glob(REMOTE_FILES_DIR):
                if file_name.endswith('.crdownload') or file_name.endswith('.part'):
                    download_timer = True
            seconds += 1
        sleep(2)
        return seconds

    def check_quantity_of_downloaded_files(self, quantity_of_files):
        sleep(2)
        self.open_new_tab()
        self.switch_to_new_tab()
        self.browser.wd.get(f"file://{REMOTE_FILES_DIR}")
        self.wait_visible(Locator(xpath="//table/tbody[@id='tbody']"))
        download_files = len(self.find_all(Locator(xpath="//a[@class='icon file']")))
        assert quantity_of_files == download_files, \
            f"Ожидаемое кол-во загруженных файлов '{quantity_of_files}' не соответствует найденному '{download_files}'"
        self.close_last_tab()

    def check_downloaded_files(self, storage, file_name: str, is_same: int = None, storage_directory: dir = None):
        sleep(2)

        if storage == 'local':
            storage_directory = f"/{LOCAL_FILES_DIR}"
        elif storage == 'chrome':
            storage_directory = REMOTE_FILES_DIR

        self.open_new_tab()
        self.switch_to_new_tab()
        self.browser.wd.get(f"file://{storage_directory}")
        self.wait_visible(Locator(xpath="//table/tbody[@id='tbody']"))

        if is_same:
            if file_name == "download":
                same_file_name = file_name + f" ({is_same})"
            else:
                same_file_name = re.sub(r'(?=[.,])(?=[^\s])', fr' ({is_same})', file_name)

            self.browser.asserts.assert_downloaded_file_present(
                locator=Locator(xpath=f"//tbody[@id='tbody']//a[contains(text(), '{same_file_name}')]"),
                retries=1)
        else:
            self.browser.asserts.assert_downloaded_file_present(
                locator=Locator(xpath=f"//tbody[@id='tbody']//a[contains(text(), '{file_name}')]"),
                retries=1)

        self.close_last_tab()

    def download_file_from_remote(self, filename: str):
        current_session = self.get_session_id()
        page_url = f"{SELENOID_DOWNLOAD}{current_session}/{filename}"

        with open(f"{LOCAL_FILES_DIR}/" + filename, "wb") as file:
            response = requests.get(page_url)
            file.write(response.content)
