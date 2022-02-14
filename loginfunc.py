import math
import time
from ctypes import cast

import pyautogui
import selenium
from decouple import config
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from helpers import wait_for_selector, wait_for_xpath

proxy_username = config("PROXY_USER", cast=str)
proxy_password = config("PROXY_PASSWORD", cast=str)

freelancer_email = config("USER_NAME", cast=str)
freelancer_password = config("USER_PASWORD", cast=str)


def login(chrome_driver, email, password):
    try:
        login_button_xpath = "//a[contains(text(), 'Log In')]"
        wait_for_xpath(xpath=login_button_xpath, timeout=5, driverr=chrome_driver)
        chrome_driver.find_element_by_xpath(login_button_xpath).click()
        email_input_selector = "body > app-root > app-logged-out-shell > app-login-page > fl-container > fl-bit > app-login > app-credentials-form > form > fl-input.ng-tns-c189-10.ng-star-inserted > fl-bit > fl-bit > fl-bit > input"
        wait_for_selector(selector=email_input_selector, timeout=5, driverr=chrome_driver)
        chrome_driver.find_element_by_css_selector(email_input_selector).send_keys(email)
        chrome_driver.find_element_by_css_selector(
            "body > app-root > app-logged-out-shell > app-login-page > fl-container > fl-bit > app-login > app-credentials-form > form > fl-input.ng-tns-c189-11.ng-star-inserted > fl-bit > fl-bit > fl-bit > input"
        ).send_keys(password)
        chrome_driver.find_element_by_xpath(".//*[contains(text(), 'Remember me')]").click()
        time.sleep(4)
        chrome_driver.find_element_by_css_selector(
            "body > app-root > app-logged-out-shell > app-login-page > fl-container > fl-bit > app-login > app-credentials-form > form > app-login-signup-button > fl-button > button"
        ).click()
        time.sleep(50)
    except Exception as e:
        print(e)
        print("already logged in")


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


def loaded_browser():
    driver = initialize_driver()
    login(driver, freelancer_email, freelancer_password)
    return driver
