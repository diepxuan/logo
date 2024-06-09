import time
import configparser
import shutil

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from datetime import datetime, timedelta

import __string as string
import __url as url
import __os as os


def configPath(path):
    if path:
        return os.path.join(os.dirImg(path, make=True), "config.ini")
    return os.path.join(os.dirImg(), "config.ini")


def set(config=configparser.ConfigParser()):
    if not valid(config):
        return
    path = config["DEFAULT"]["path"]
    with open(configPath(path), "w") as configfile:
        config.write(configfile)
    return config


def get(path="") -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    try:
        config.read(configPath(path))
    except:
        config = configparser.ConfigParser(strict=False)
        config.read(configPath(path))
    finally:
        config["DEFAULT"]["path"] = path
    return config


def isOld(path, days=1) -> bool:
    return __olded(path, scope="DEFAULT", days=1)


def isSearchOld(path, days=1) -> bool:
    return __olded(path, scope="search", days=1)


def isImagesOld(path, days=1) -> bool:
    return __olded(path, scope="images", days=1)


def __olded(path, scope="DEFAULT", days=1) -> bool:
    config = get(path)
    if not config.has_section(scope):
        if scope != "DEFAULT":
            config.add_section(scope)
        config[scope]["lastOpen"] = (datetime.now() - timedelta(10)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    return datetime.strptime(
        config[scope]["lastOpen"], "%Y-%m-%d %H:%M:%S"
    ) < datetime.now() - timedelta(days)


def valid(config: configparser.ConfigParser):
    return url.valid(config["DEFAULT"]["url"])


def remove(path):
    try:
        shutil.rmtree(os.dirImg(path))
        print(f"Folder '{os.dirImg(path)}' removed successfully.")
        return True
    except OSError as e:
        print(f"Error removing folder: {e}")
        return False
