from urllib.parse import urlparse


def valid(url) -> bool:
    try:
        result = urlparse(f"{url}")
        return all([result.scheme, result.netloc])
    except:
        return False
