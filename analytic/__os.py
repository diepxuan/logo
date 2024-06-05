from os import *


def dirRoot(_path):
    rootPath = getcwd()
    if _path:
        imgPath = path.abspath(path.join(rootPath, _path))
    return imgPath


def dirSrc():
    return dirRoot("src")
    print(path.dirname(path.abspath(__file__)))


def dirImg(_path="", make=False):
    imgPath = dirRoot("images")
    if make and not path.exists(imgPath):
        makedirs(imgPath)
    if _path:
        imgPath = path.join(imgPath, _path)
        if make and not path.exists(imgPath):
            makedirs(imgPath)
    return imgPath


def fromFile(_path=""):
    with open(_path, "r") as f:
        lines = f.readlines()
    return lines


def toFile(_path="", _data=[]):
    with open(_path, "w") as f:
        for item in _data:
            f.write(item + "\n")
