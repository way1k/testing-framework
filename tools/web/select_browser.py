from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class BrowserTypes:
    """
    Supported browser types
    """
    CHROME = "chrome"
    FIREFOX = "firefox"
    SAFARI = "safari"


def local(browser):
    """Returns local browser instance."""

    if browser == BrowserTypes.CHROME:
        options = ChromeOptions()
        # options.set_capability("acceptInsecureCerts", True)
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    elif browser == BrowserTypes.FIREFOX:
        options = FirefoxOptions()
        # options.set_capability("acceptInsecureCerts", True)
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_options=options)
    elif browser == BrowserTypes.SAFARI:
        driver = webdriver.Safari()
    else:
        raise ValueError(f"Unknown browser type: {browser}")
    return driver


def remote(browser, path):
    """Returns remote driver instance"""

    if browser == BrowserTypes.CHROME:
        caps = DesiredCapabilities.CHROME
    elif browser == BrowserTypes.FIREFOX:
        caps = DesiredCapabilities.FIREFOX
    else:
        raise ValueError(f"Unknown browser type: {browser}")

    # caps["acceptInsecureCerts"] = True
    driver = webdriver.Remote(command_executor=path, desired_capabilities=caps)

    return driver
           # webdriver.Remote(command_executor="http://selenium__standalone-chrome:4444/wd/hub")
