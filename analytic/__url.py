from urllib.parse import urlparse


def valid(url) -> bool:
    try:
        urlparse(url)
        return True
    except:
        return False
