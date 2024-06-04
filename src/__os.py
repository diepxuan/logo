from os import *


def dirRoot(_path):
    rootPath = getcwd()
    if _path:
        imgPath = path.abspath(path.join(rootPath, _path))
    return imgPath


def dirSrc():
    return dirRoot("src")
    print(path.dirname(path.abspath(__file__)))


def dirImg(_path=""):
    imgPath = dirRoot("images")
    if not path.exists(imgPath) and not path.isdir(imgPath):
        makedirs(imgPath)
    if _path:
        imgPath = path.join(imgPath, _path)
        print(imgPath)
        if not path.exists(imgPath) or not path.isdir(imgPath):
            makedirs(imgPath)
    return imgPath
