import time

import pyautogui
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

proxy_username = "uaihulfj"
proxy_password = "7DrHZ3bsrYpbuw9B"


def initialize_driver():
    caps = DesiredCapabilities.CHROME
    caps["goog:loggingPrefs"] = {"performance": "ALL"}
    option = Options()
    option.add_argument("--disable-infobars")
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_argument(
        "'user-agent'= 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'"
    )
    # option.add_argument('--headless')
    # option.add_argument("window-size=1920x1080")
    option.add_argument("--disable-crash-reporter")
    option.add_argument("--disable-in-process-stack-traces")
    option.add_argument("--disable-logging")
    option.add_argument("--disable-dev-shm-usage")
    option.add_argument("--log-level=3")
    option.add_argument("start-maximized")
    option.add_argument("--proxy-server=52.55.139.214:31112")
    option.add_argument("--disable-extensions")
    # explore Path lib for this
    option.add_argument("user-data-dir=C:\\Users\\hamza.idrees\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 5")
    option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
    initialized_driver = webdriver.Chrome(
        executable_path="chromedriver.exe", options=option, desired_capabilities=caps
    )

    # logging in to proxy ip
    initialized_driver.get("https://www.freelancer.com/")
    time.sleep(5)
    initialized_driver.get("https://www.freelancer.com/")
    time.sleep(5)
    pyautogui.typewrite(proxy_username)
    pyautogui.press("tab")
    pyautogui.typewrite(proxy_password)
    pyautogui.press("enter")
    return initialized_driver
