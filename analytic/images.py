import time
import configparser
import random
import uuid

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
    ElementClickInterceptedException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlparse, unquote
from unidecode import unidecode
from datetime import datetime, timedelta
from urllib.request import urlretrieve

import __string as string
import __os as os
import __config as config
import __levenshtein as levenshtein
import __url as url

lstExcept = [
    "DEFAULT",
    "search",
    "images",
]
step_max = 50
step_index = 0
driver: webdriver.Chrome = None


def crawl():
    """product images searching"""
    global driver
    driver = __browserOpen()
    paths = os.listdir(os.dirImg())
    random.shuffle(paths)
    for item in [item for item in paths if os.path.isdir(os.dirImg(item))]:
        __images_init(item)
    __browserClose(driver)


def __images_init(path):
    if step_index > step_max:
        # pass
        return
    if not config.isImagesOld(path):
        return
    if not config.valid(config.get(path)):
        return
    __images_looking(path)


def __images_looking(path):
    xpath = config.get()
    cnf = config.get(path)
    for section in [
        section
        for section in cnf.sections()
        if section not in lstExcept
        and section in xpath.sections()
        and url.valid(cnf[section]["url"])
    ]:
        _url = cnf[section]["url"]
        print(f"search [{path}] images")
        print(f"  from [{section}]")
        print(f"  over {_url}")
        __images_open(section)(path)
    # __step_index()
    if not cnf.has_section("images"):
        cnf.add_section("images")
    cnf["images"]["lastSearch"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def __images_open_nemgiakho_com(path):
    section = "nemgiakho.com"
    xpath = config.get()[section]["xpath"]
    cnf = config.get(path)
    url = cnf[section]["url"]
    driver.get(url)
    # driver.save_screenshot("screenshot.png")
    try:
        # container = driver.find_element(By.CSS_SELECTOR, ".category-description")
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except:
        return

    pics = container.find_elements(By.TAG_NAME, "img")
    for pic in pics:
        src = pic.get_attribute("src")
        print(f"   * {src}")
        filename = src.split("/")[-1]
        if not filename or any(
            char in filename for char in ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
        ):
            filename = f"{uuid.uuid4()}.jpg"
        save_path = os.path.join(os.dirImg(path), filename)
        urlretrieve(src, save_path)


def __images_open_everonvn_com_vn(path):
    section = "everonvn.com.vn"
    xpath = config.get()[section]["xpath"]
    cnf = config.get(path)
    url = cnf[section]["url"]
    driver.get(url)
    try:
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except:
        return

    pics = container.find_element(By.CSS_SELECTOR, "div.viewimage")
    pics = pics.get_attribute("data-img")
    pics = pics.split(",")
    for pic in [pic.strip("/") for pic in list(set(pics)) if len(pic.strip())]:
        src = f"https://everonvn.com.vn/{pic}"
        print(f"   * {src}")
        __images_save(path, src)


def __images_save(path, src):
    filename = src.split("/")[-1]
    if not filename or any(
        char in filename for char in ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
    ):
        filename = f"{uuid.uuid4()}.jpg"
    save_path = os.path.join(os.dirImg(path), filename)
    urlretrieve(src, save_path)
    __step_index()


def __images_open_everonhanquoc_vn(path):
    section = "everonhanquoc.vn"
    xpath = config.get()[section]["xpath"]
    cnf = config.get(path)
    url = cnf[section]["url"]
    driver.get(url)
    # driver.save_screenshot("screenshot.png")
    try:
        # container = driver.find_element(By.CSS_SELECTOR, ".category-description")
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".category-description"))
        )
    except:
        container = None
    try:
        if not container:
            # container = driver.find_element(By.CSS_SELECTOR, ".product-content")
            container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".product-content .detail")
                )
            )
    except:
        return
    pics = container.find_elements(By.TAG_NAME, "img")
    for pic in pics:
        src = pic.get_attribute("src")
        print(f"   * {src}")
        __images_save(path, src)


def __images_open_shopee_vn(path):
    return
    section = "shopee.vn"
    xpath = config.get()[section]["xpath"]
    cnf = config.get(path)
    url = cnf[section]["url"]
    print(f"search images from {url}")
    driver.get(url)
    time.sleep(5)
    # driver.save_screenshot("screenshot.png")
    # body = driver.find_element(By.TAG_NAME, "body")
    wait = WebDriverWait(driver, 10)
    # result = wait.until(EC.presence_of_element_located((By.ID, "modal")))
    result = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    # result = wait.until(
    #     EC.presence_of_element_located((By.XPATH, '//div[@id="modal"]'))
    # )
    # pics = driver.find_elements_by_css_selector(
    #     "#modal .shopee-image-container picture img"
    # )
    pics = result.find_elements(
        By.CSS_SELECTOR, "#modal .shopee-image-container picture img"
    )
    # pics = result.find_elements(By.TAG_NAME, "picture")
    # result = driver.find_element(By.ID, "modal")
    # result = result[0].find_elements(By.TAG_NAME, "picture")
    # html_content = result.get_attribute("innerHTML")
    # print(html_content)
    # return
    print(pics)
    # for pic in result.find_elements(By.TAG_NAME, "picture"):
    for pic in pics:
        print(pic)
        # img = pic.find_element(By.TAG_NAME, "img")
        print(pic.get_attribute("src"))
    # result.find_elements(By.TAG_NAME, "img")
    # img_url = result.get_attribute("src")
    # print(img_url)
    # driver.close()
    # driver.n


def __browserClose(driver: webdriver.Chrome):
    # driver.close()
    driver.close()


def __browserOpen(url="") -> webdriver.Chrome:
    mode = os.environ.get("MODE", "developer")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.implicitly_wait(2)
    if url:
        driver.get(url)
    return driver


def __images_open(section):
    try:
        functions = {
            "shopee.vn": __images_open_shopee_vn,
            "everonhanquoc.vn": __images_open_everonhanquoc_vn,
            "nemgiakho.com": __images_open_nemgiakho_com,
            "everonvn.com.vn": __images_open_everonvn_com_vn,
        }
        function = functions[section]
        return function
    except:
        pass


def __step_index():
    global step_index
    step_index += 1
