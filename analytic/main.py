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
from search import Search


def crawl():

    Page(url=f"https://www.diepxuan.com").crawl()


def images():
    Search(url=f"https://www.diepxuan.com").crawl()


def run_as_type():
    _type = os.environ.get("TYPE", "crawl")
    match _type:
        case "crawl":
            crawl()
        case "images":
            images()
        case _:
            crawl()


if __name__ == "__main__":
    run_as_type()
