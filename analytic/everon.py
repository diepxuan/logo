import time
import configparser
import random

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)

from urllib.parse import urlparse
from datetime import datetime, timedelta

import __string as string
import __os as os
import __config as config
import __url as Url

dev_mode = os.environ.get("MODE", "dev") == "dev"

config_file = os.path.join(os.dirData(), "config.ini")
product_config = configparser.ConfigParser(strict=False)
product_config.read(config_file)

domain = "everon.com"
base_url = f"https://{domain}/"

step_max = 20
step_index = 0
driver: webdriver.Chrome = None

if "products" not in product_config:
    product_config["products"] = {}
if "excluded" not in product_config:
    product_config["excluded"] = {
        "pages": "",
    }
else:
    excluded_pages = product_config["excluded"]["pages"].split("\n")

with open(config_file, "w") as f:
    product_config.write(f)

visited_pages = set()
visited_pages.update(excluded_pages)
waiting_pages = []


def __crawl():
    global step_index, driver, waiting_pages

    _log("waiting page loaded")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "app")))
    time.sleep(random.uniform(5, 8))  # Sleep ngẫu nhiên để "giống người dùng"

    page_link = driver.current_url.split("#")[0].rstrip("/")
    # path = page_link.split("/")[-1].split(".")[0]
    visited_pages.add(page_link)
    _log(f"Visited: {driver.title} - {driver.current_url}")

    if _is_product_page():
        sku = _product_sku()
        if sku and sku not in product_config["products"]:
            print(f"  [✓] New product found: {sku} - {page_link}")
            _product_save(sku, page_link)
            product_config["products"][sku] = page_link
            _save_product_list()
            step_index += 1

    if step_index > step_max:
        _log(f"{step_index} > {step_max}")
        return

    # links = driver.find_elements(By.CSS_SELECTOR, "body a")
    links = [
        a
        for a in driver.find_elements(By.CSS_SELECTOR, "body a")
        if (href := a.get_attribute("href"))
        and href.startswith("http")
        and not href.lower().endswith(
            (".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp")
        )
    ]

    hrefs = [
        (link.get_attribute("href") or "").split("#")[0].rstrip("/") for link in links
    ]
    # hrefs = [href for href in hrefs if _is_valid_url(href, page_link)]
    # hrefs = list(set(filter(None, hrefs)))  # Remove None và duplicates
    waiting_pages = waiting_pages + hrefs
    waiting_pages = [href for href in waiting_pages if _is_valid_url(href, page_link)]
    waiting_pages = list(set(filter(None, waiting_pages)))

    while waiting_pages:
        href = random.choice(waiting_pages)
        try:
            safe_href = href.replace("'", "&apos;")
            link = driver.find_element(By.XPATH, f"//a[@href={safe_href}]")
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                link,
            )  # Cuộn đến phần tử trước khi click
            link.click()
            return __crawl()
        except:
            if goto(href):
                return __crawl()

    # Nếu không còn link nào hợp lệ, quay lại trang chủ
    try:
        driver.find_element(By.CSS_SELECTOR, "header a.header__logo").click()
        return __crawl()
    except:
        if goto(base_url):
            return __crawl()


def crawl():
    global driver
    __browserOpen()
    driver.get(base_url)
    # driver.get("https://everon.com/san-pham/chan-dual-comfort")
    __crawl()
    __browserClose()
    _save_product_list()


def __browserOpen() -> webdriver.Firefox:
    global driver
    __browserClose
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


def __browserClose():
    global driver
    driver.quit()


def _is_valid_url(link, current):
    if not link:
        return False
    if link == current:
        return False
    link = link.split("#")[0].rstrip("/")
    if not Url.valid(link):
        return False
    if link in visited_pages:
        return False
    if any(exc in link for exc in excluded_pages):
        return False
    if any(link.startswith(exc) for exc in excluded_pages):
        return False
    if not link.startswith(base_url):
        return False
    return True


def _is_product_page():
    try:
        return bool(_product_sku())
    except:
        return False


def _product_sku():
    try:
        xpath_sku = "//div[@class=product-detail-page]//div[@class=product-information]//div[@class=sku]"
        sku_elem = driver.find_element(By.XPATH, xpath_sku)
        return sku_elem.text.strip()
    except:
        # fallback dùng đường dẫn cuối cùng của URL
        return False


def _save_product_list():
    with open(config_file, "w") as f:
        product_config.write(f)


def _product_save(sku, url):
    product_file = os.path.join(os.dirData(), f"{sku}.ini")
    cfg = configparser.ConfigParser()
    cfg["info"] = {
        "sku": sku,
        "url": url,
        "lastOpen": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(product_file, "w") as f:
        cfg.write(f)


def goto(url):
    if driver.current_url != url:
        driver.get(url)
        return True
    return False


def _log(messenger):
    if not dev_mode:
        return
    print(f"{datetime.now()} {messenger}")
