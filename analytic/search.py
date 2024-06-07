import time
import datetime
import configparser

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlparse
from unidecode import unidecode

import __string as string
import __os as os
import __levenshtein as levenshtein


def crawl():
    for item in [
        item for item in os.listdir(os.dirImg()) if os.path.isdir(os.dirImg(item))
    ]:
        __search_init(item)


def __search_init(path):
    # path = os.dirImg(path)
    title = path.replace("-", " ")
    print(f"Searching {title}")
    mode = os.environ.get("MODE", "developer")
    options = Options()
    firefox_profile = FirefoxProfile()
    firefox_profile.set_preference("javascript.enabled", mode == "product")
    options.profile = firefox_profile
    options.add_argument("-headless")
    # options.add_argument("--new-window")

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(2)

    # try:
    __search_query(driver, title)
    # except NoSuchElementException as e:
    # print(e)

    driver.quit()


def __search_query(driver: webdriver.Firefox, path):
    title = path.replace("-", " ")
    print(f"Searching {title}")

    driver.get("https://www.google.com/")
    cnf = config.get(path)
    cnf["search"]["lastSearch"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config.set(cnf)
    wait = WebDriverWait(driver, 10)

    search_xpath = "//textarea[@name='q']"
    search_field = wait.until(EC.presence_of_element_located((By.XPATH, search_xpath)))
    search_field.send_keys(title)
    search_field.send_keys(Keys.ENTER)

    result_xpath = "//div[@id='search']/div/div/div"
    search_results = wait.until(EC.presence_of_element_located((By.ID, "search")))
    body = driver.find_element(By.TAG_NAME, "body")
    for i in range(5):
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    search_results = driver.find_elements(By.XPATH, result_xpath)
    for search_result in [
        search_result for search_result in search_results if search_result.text.strip()
    ]:
        try:
            search_element = search_result.find_element(By.TAG_NAME, "a")
            search_url = search_element.get_attribute("href")
            search_title = search_result.find_element(By.TAG_NAME, "h3").text
            search_text = search_result.find_element(By.TAG_NAME, "cite").text
            search_match = levenshtein.percentage(
                unidecode(search_title).lower(), title
            )
            search_match_txt = "{:.1f}%".format(search_match)
            print(f" * {search_match_txt} {search_title}")
            print(f"   - {search_text}")
            print(f"   - {search_url}")
            if search_match < 70:
                continue
            search_element.click()
            time.sleep(3)
            body = driver.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            body.send_keys(Keys.PAGE_DOWN)
            break
        except NoSuchElementException:
            continue
        except StaleElementReferenceException:
            continue


def __browserClose(driver: webdriver.Firefox):
    driver.quit()


def __browserOpen() -> webdriver.Firefox:
    mode = os.environ.get("MODE", "developer")
    options = Options()
    firefox_profile = FirefoxProfile()
    firefox_profile.set_preference("javascript.enabled", mode == "product")
    options.profile = firefox_profile
    options.add_argument("-headless")
    # options.add_argument("--new-window")
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(2)


step_max = 50
step_index = 0
