#!/usr/bin/env python3
#!/usr/bin/env python

import datetime
import re
import sys
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import __os as os
from page import Page


def crawl():
    mode = os.environ.get("MODE", "developer")
    options = Options()
    firefox_profile = FirefoxProfile()
    firefox_profile.set_preference("javascript.enabled", mode == "product")
    options.profile = firefox_profile
    options.add_argument("-headless")

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(2)
    Page(driver, url=f"https://www.diepxuan.com").crawl()
    driver.quit()


if __name__ == "__main__":
    crawl()
