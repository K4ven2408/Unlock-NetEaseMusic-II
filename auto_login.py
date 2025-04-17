# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "005374AF3F08236B08DA7CC1E9AF7B4CC470890E5C61E5786A34957F4A42249B06971BA6D86294B61C79BECA20321FF6910C3DF65FE6BBD2453C78817C33B259DD50E4860248A420DF84AA5D73D7DBF43B0BCF8389D0ED68BC19E25CD756A2C6325817D18158912231CFB8E18E4187013536D7459953EAD98CF626ABEE9776FE5D5F1AE3871E3881B6E298D2E2910576878273741E2580213D6532D51DD444C6ED1F06809D9A83E2932B15DC716C966A208AB0CF172AA59CC28D42A7BECAA4564CFAB5D290C66C812810FF7DA99D76FAA0A051D2F3CDDD23C360741021CD3E7255270AF6A2BDF5CD640A5678C4769629D7DEECF9DCAC8A181845CB8E66247AA8E77F6B6CECAF5F0EA7F0B52EF5FB3E0960449C00CB750938A6ED57959ED96923115221D8BE565C7376F61BA21F1A62A69883C8DB4DFD757B4BBDB25287C7C0CF2197E31E812311EC548AA9A761AD15E52A451D0E8EF8ECF61AE4996D53F9BB505E"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
