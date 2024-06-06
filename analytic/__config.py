import time
import configparser

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from datetime import datetime, timedelta

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


def isOld(path) -> bool:
    config = get(path)
    try:
        return datetime.strptime(
            config["DEFAULT"]["lastOpen"]
        ) < datetime.now() - timedelta(days=2)
    except:
        return True


lstConfig = list
for item in [
    item
    for item in os.listdir(os.dirImg(make=True))
    if os.path.isdir(os.dirImg(item, make=True))
]:
    config = configparser.ConfigParser().read(configPath(item))
    config["DEFAULT"]["path"] = item
    lstConfig.append(config)
