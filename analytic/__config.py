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
import __os as os


def configPath(path):
    return os.path.join(os.dirImg(path, make=True), "config.ini")


def set(config=configparser.ConfigParser()):
    path = config["DEFAULT"]["path"]
    with open(configPath(path), "w") as configfile:
        config.write(configfile)
    return config


def get(path) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(configPath(path))
    config["DEFAULT"]["path"] = path
    return config


def isOld(path, days=1) -> bool:
    return __olded(path, scope="DEFAULT", days=1)


def isSearchOld(path, days=1) -> bool:
    return __olded(path, scope="search", days=1)


def __olded(path, scope="DEFAULT", days=1) -> bool:
    config = get(path)
    try:
        if not config.has_section(scope):
            config[scope] = {}
        return datetime.strptime(
            config[scope]["lastOpen"], "%Y-%m-%d %H:%M:%S"
        ) < datetime.now() - timedelta(days)
    except:
        return True
    finally:
        return True


def remove(path):
    try:
        shutil.rmtree(os.dirImg(path))
        print(f"Folder '{os.dirImg(path)}' removed successfully.")
        return True
    except OSError as e:
        print(f"Error removing folder: {e}")
        return False
