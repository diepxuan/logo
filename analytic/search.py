import time
import configparser
import random

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
)
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlparse, unquote
from unidecode import unidecode
from datetime import datetime, timedelta

import __string as string
import __os as os
import __config as config
import __levenshtein as levenshtein

step_max = 50
step_index = 0


def crawl():
    """searching another page about product"""
    for item in [
        item
        for item in random.shuffle(os.listdir(os.dirImg()))
        if os.path.isdir(os.dirImg(item))
    ]:
        __search_init(item)


def __search_init(path):
    if step_index > step_max:
        return
    if not config.isSearchOld(path):
        return
    if not config.valid(config.get(path)):
        return

    driver = __browserOpen()
    __search_query(driver, path)
    __browserClose(driver)


def __search_query(driver: webdriver.Firefox, path):
    global step_index

    title = path.replace("-", " ")
    print(f"Searching {title}")

    driver.get("https://www.google.com/")
    wait = WebDriverWait(driver, 10)

    cnf = config.get(path)
    if not cnf.has_section("search"):
        cnf.add_section("search")
    cnf["search"]["lastSearch"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    config.set(cnf)
    step_index += 1

    # search by title
    search_xpath = "//textarea[@name='q']"
    search_field = wait.until(EC.presence_of_element_located((By.XPATH, search_xpath)))
    search_field.send_keys(title)
    search_field.send_keys(Keys.ENTER)

    # filter DOM for search result
    result_xpath = "//div[@id='search']/div/div/div"
    search_results = wait.until(EC.presence_of_element_located((By.ID, "search")))
    body = driver.find_element(By.TAG_NAME, "body")
    for i in range(5):
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    search_results = driver.find_elements(By.XPATH, result_xpath)
    match_percent = 0
    match_element = None
    for search_result in [
        search_result
        for search_result in search_results
        if len(search_result.text.strip()) > 0
    ]:
        try:
            search_element = search_result.find_element(By.TAG_NAME, "a")
            search_url = search_element.get_attribute("href")
            search_domain = urlparse(search_url).netloc
            search_title = search_result.find_element(By.TAG_NAME, "h3").text
            search_text = search_result.find_element(By.TAG_NAME, "cite").text
            search_match = levenshtein.percentage(
                unidecode(search_title).lower(), title
            )
            search_match_txt = "{:.1f}%".format(search_match)

            # show result
            print(f" * {search_match_txt} {search_title}")
            print(f"   - {search_text}")
            print(f"   - {search_url}")

            # save config to search images
            if not cnf.has_section(search_domain):
                cnf.add_section(search_domain)
            cnf[search_domain]["match"] = f"{'{:.1f}%%'.format(search_match)}"
            cnf[search_domain]["title"] = f"{unquote(search_title).replace('%','%%')}"
            cnf[search_domain]["url"] = f"{unquote(search_url)}"
            config.set(cnf)

            # note match to go into
            if match_percent < search_match:
                match_percent = search_match
                match_element = search_element

        except NoSuchElementException:
            continue
        except StaleElementReferenceException:
            continue

    if match_percent < 70:
        return
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", match_element)
        match_element.click()
        time.sleep(1)
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.PAGE_DOWN)
        match_element = random.choice(driver.find_elements(By.TAG_NAME, "a"))
        match_element.click()
        time.sleep(1)
    except:
        return


def __browserClose(driver: webdriver.Firefox):
    # driver.close()
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
    return driver
