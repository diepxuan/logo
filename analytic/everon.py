import time
import configparser
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlparse
from datetime import datetime, timedelta

import __string as string
import __os as os
import __config as config
import __url as Url


domain = "everon.com"
base_url = f"https://{domain}/"
visited_pages = []
excluded_pages = [
    "https://everon.com/faq",
    "https://everon.com/contact",
    "https://everon.com/privacy-policy",
    "https://everon.com/terms-of-service",
    "https://everon.com/careers",
    "https://everon.com/blog",
    "https://everon.com/about-us",
]
step_max = 5000
step_index = 0
driver: webdriver.Chrome = None

config_file = os.path.join(os.dirData(), "config.ini")
product_config = configparser.ConfigParser()
product_config.read(config_file)
if "products" not in product_config:
    product_config["products"] = {}


def __crawl():
    global step_index, driver
    print(f"{datetime.now()} Visited: {driver.title} - {driver.current_url}")

    page_link = driver.current_url.split("#")[0].rstrip("/")
    # path = page_link.split("/")[-1].split(".")[0]
    if _is_product_page():
        sku = _get_product_sku()
        if sku and sku not in product_config["products"]:
            product_config["products"][sku] = page_link
            _save_product_detail(sku, page_link)

        step_index += 1
        visited_pages.append(page_link)

    if step_index > step_max:
        return

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.TAG_NAME, "main"))
    )
    links = driver.find_elements(By.CSS_SELECTOR, "body a")
    links = list(set(links))  # Remove duplicates

    while links:
        link = random.choice(links)
        href = link.get_attribute("href")
        href = href.split("#")[0].rstrip("/") if href else None

        if _is_valid_url(href, page_link):
            try:
                link.click()
                time.sleep(10)
                return __crawl()
            except:
                pass
        links.remove(link)

    # Nếu không còn link nào hợp lệ, quay lại trang chủ
    try:
        driver.find_element(By.CSS_SELECTOR, "header a.header__logo").click()
        time.sleep(10)
    except:
        pass

def crawl():
    global driver
    __browserOpen()
    driver.get(base_url)
    __crawl()
    __browserClose()
    _save_product_list()

def __browserOpen():
    global driver
    mode = os.environ.get("MODE", "developer")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.implicitly_wait(5)
    return driver


def __browserClose():
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
    if not link.startswith(base_url):
        return False
    return True


def _is_product_page():
    try:
        xpath = "//div[@class='product-information']//div[@class='sku']"
        title = driver.find_element(By.XPATH, xpath).text
        return bool(title)
    except:
        return False

def _get_product_sku():
    try:
        # Tùy chỉnh lấy SKU nếu có thẻ cụ thể, hoặc fallback dùng slug
        # Ví dụ: <div class="product sku">SKU12345</div>
        sku_elem = driver.find_element(By.CSS_SELECTOR, ".product-detail-page .product-information .sku")
        return sku_elem.text.strip()
    except:
        # fallback dùng đường dẫn cuối cùng của URL
        return driver.current_url.rstrip("/").split("/")[-1].split(".")[0]

def _save_product_list():
    with open(config_file, "w") as f:
        product_config.write(f)

def _save_product_detail(sku, url):
    product_file = os.path.join(os.dirData(), f"{sku}.ini")
    cfg = configparser.ConfigParser()
    cfg["DEFAULT"] = {
        "url": url,
        "lastOpen": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(product_file, "w") as f:
        cfg.write(f)