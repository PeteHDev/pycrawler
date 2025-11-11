from urllib.parse import urlparse

def normalize_url(url):
    parsed = urlparse(url)
    return parsed.hostname + parsed.path.rstrip("/")