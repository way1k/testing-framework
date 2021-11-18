from selenium import webdriver
from tools.web_asserts import Asserts
from tools.browser.browser_methods import BrowserMethods
from pages.pages_init import Bashorg, Reqres
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from settings import LOCAL_FILES_DIR, REMOTE_FILES_DIR, SELENOID_ENDPOINT


class Browser:
    """
    Класс инициализации объекта веб-драйвера
    """

    def __init__(self, browser, browser_version, bash_url, reqres_url, test_name):

        if browser in ("local", "chrome", "firefox"):
            self.wd = self.driver_setup(
                browser=browser,
                version=browser_version,
                test_name=test_name
            )
        else:
            raise ValueError(f"Указанный тип браузера '{browser}' не поддерживается")

        self.bash_url = bash_url
        self.reqres_url = reqres_url
        self.browser_methods = BrowserMethods(self)
        self.asserts = Asserts(self)

        self.bash_org = Bashorg(self)
        self.reqres = Reqres(self)

    @staticmethod
    def driver_setup(browser: str, version: str, test_name: str):
        driver = None
        capabilities = {
            "browserName": browser,
            "version": version,
            "enableVNC": True,
            "enableVideo": False,
        }

        if capabilities["browserName"] == 'local':
            chrome_local_options = ChromeOptions()
            chrome_local_options.set_capability("name", test_name)
            chrome_local_options.set_capability("acceptInsecureCerts", True)
            chrome_local_options.add_experimental_option("excludeSwitches", ["enable-automation"])

            chrome_local_options.add_experimental_option(
                "prefs", {
                    "download.default_directory": f"{LOCAL_FILES_DIR}",
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing_for_trusted_sources_enabled": False,
                    "safebrowsing.enabled": False,
                    "download.safebrowsing.enabled": True,
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False
                }
            )

            driver = webdriver.Chrome(chrome_options=chrome_local_options)

        elif capabilities["browserName"] == 'chrome':
            chrome_remote_options = ChromeOptions()
            chrome_remote_options.set_capability("name", test_name)
            chrome_remote_options.add_argument("--disable-gpu")
            chrome_remote_options.add_argument("--no-sandbox")
            chrome_remote_options.add_argument("--disable-setuid-sandbox")
            chrome_remote_options.add_experimental_option("excludeSwitches", ["enable-automation"])

            chrome_remote_state_prefs = {
                "browser": {
                    "enabled_labs_experiments": [
                        "treat-unsafe-downloads-as-active-content@2"
                    ],
                }
            }

            chrome_remote_options.add_experimental_option(
                "localState", chrome_remote_state_prefs)

            chrome_remote_options.add_experimental_option(
                "prefs", {
                    "download.default_directory": f"{REMOTE_FILES_DIR}",
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "safebrowsing.enabled": False,
                    "download.safebrowsing.enabled": False,
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False
                }
            )

            driver = webdriver.Remote(
                command_executor=SELENOID_ENDPOINT,
                desired_capabilities=capabilities,
                options=chrome_remote_options)

        elif capabilities["browserName"] == 'firefox':
            firefox_remote_options = FirefoxOptions()
            firefox_remote_options.set_capability("acceptInsecureCerts", True)
            firefox_remote_options.set_capability("name", test_name)

            firefox_remote_profile = FirefoxProfile()

            driver = webdriver.Remote(
                command_executor=SELENOID_ENDPOINT,
                desired_capabilities=capabilities,
                options=firefox_remote_options,
                browser_profile=firefox_remote_profile)

        driver.maximize_window()
        return driver
