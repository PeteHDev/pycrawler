from urllib.parse import urlparse
from bs4 import BeautifulSoup

def normalize_url(url):
    parsed = urlparse(url)
    return parsed.hostname + parsed.path.rstrip("/")

def get_h1_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    first_header = soup.find("h1")
    if first_header is None:
        return ""
    return first_header.get_text()

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    if main is None:
        first_paragraph = soup.find("p")
        if first_paragraph is None:
            return ""
        return first_paragraph.get_text()
    
    first_paragraph = main.find("p")
    if first_paragraph is None:
        return ""
    return first_paragraph.get_text()