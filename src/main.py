#!/usr/bin/env python3
#!/usr/bin/env python

import datetime
import re
import sys
import time
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

LOGTYPE = {"INFO": "INFO", "ERROR": "ERROR"}


def log(mes, log_type=LOGTYPE["INFO"]):
    print(log_type, datetime.datetime.now(), mes)


options = Options()
firefox_profile = FirefoxProfile()
firefox_profile.set_preference("javascript.enabled", False)
options.profile = firefox_profile
options.add_argument("-headless")

website_url = "https://www.diepxuan.com"
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(2)
driver.get(website_url)

title = driver.title
print(title)
links = driver.find_elements(By.TAG_NAME, "a")

# navigation

for link in links:
    time.sleep(1)
    link_url = link.get_attribute("href")
    if link_url:
        time.sleep(1)
        driver.get(link_url)
        print(f"Visited: {link_url}")
        # log(f"Visited: {link_url}")

driver.quit()
