import time
import datetime
import configparser

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from urllib.parse import urlparse

import __string as string
import __os as os


def configPath(path):
    return os.path.join(os.dirImg(item, make=True), "config.ini")


def set(path, config=configparser.ConfigParser()):
    global lstConfig
    with open(configPath(path), "w") as configfile:
        config.write(configfile)
    config["DEFAULT"]["path"] = path
    lstConfig.append(config)
    return config


def get(path) -> configparser.ConfigParser:
    if any(item for item in lstConfig if item["DEFAULT"]["path"] == path):
        return [item for item in lstConfig if item["DEFAULT"]["path"] == path][0]
    return set(path)


lstConfig = list
for item in [
    item for item in os.listdir(os.dirImg()) if os.path.isdir(os.dirImg(item))
]:
    config = configparser.ConfigParser().read(configPath(item))
    config["DEFAULT"]["path"] = item
    lstConfig.append(config)
