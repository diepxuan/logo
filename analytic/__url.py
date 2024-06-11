from urllib.parse import urlparse


def valid(url) -> bool:
    """Check url is valid or not"""
    try:
        result = urlparse(f"{url}")
        return all([result.scheme, result.netloc])
    except:
        return False
