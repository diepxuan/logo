#!/usr/bin/env python3
#!/usr/bin/env python

import datetime
import re
import sys
import time
import os
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class Page:
    def __init__(self, driver: webdriver.Firefox, url):
        self.driver = driver
        self.url = urlChecker(url)

    def links(self):
        global lstPage
        links = []
        time.sleep(1)
        self.driver.get(self.url)
        lstPage = lstPage + [self.url]
        print(f"{datetime.datetime.now()} Visited: {self.driver.title} - {self.url}")
        for link in self.driver.find_elements(By.TAG_NAME, "a"):
            url = link.get_attribute("href")
            if url:
                links = links + [urlChecker(url)]
        return list(set(links))

    def crawl(self):
        if len(urlChecker(self.url).strip()) == 0:
            return
        for url in [url for url in self.links() if url not in lstPage]:
            Page(self.driver, url).crawl()


def urlChecker(url):
    url = url.split("#")[0].rstrip("/")
    if not urlparse(url).netloc == domain:
        return ""
    if url in lstPage:
        return ""
    if not any(item not in url for item in lstExcept):
        return ""
    return url


options = Options()
firefox_profile = FirefoxProfile()
firefox_profile.set_preference("javascript.enabled", False)
options.profile = firefox_profile
options.add_argument("-headless")

domain = "www.diepxuan.com"
lstPage = []
lstExcept = [
    "diepxuan.com/customer/account",
    "diepxuan.com/customer/account",
]

driver = webdriver.Firefox(options=options)
driver.implicitly_wait(2)
Page(driver, f"https://www.diepxuan.com").crawl()
driver.quit()
