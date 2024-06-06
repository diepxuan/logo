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


def set(path, config=configparser.ConfigParser()):
    with open(configPath(path), "w") as configfile:
        config.write(configfile)
    config["DEFAULT"]["path"] = path
    return config


def get(path) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(configPath(path))
    config["DEFAULT"]["path"] = path
    return config


def isOld(path) -> bool:
    config = get(path)
    try:
        return datetime.strptime(
            config["DEFAULT"]["lastOpen"], "%Y-%m-%d %H:%M:%S"
        ) < datetime.now() - timedelta(days=1)
    except:
        return True


def remove(path):
    try:
        shutil.rmtree(os.dirImg(path))
        print(f"Folder '{os.dirImg(path)}' removed successfully.")
        return True
    except OSError as e:
        print(f"Error removing folder: {e}")
        return False
