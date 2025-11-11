from urllib.parse import urlparse, urljoin
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

def extract_urls(links, base_url, look_for="href"):
    urls = []
    for link in links:
        val = link.get(look_for)
        if not val:
            continue
        ref = link.get(look_for).strip()
        if not ref:
            continue
        url = urljoin(base_url, ref)
        scheme = url.split(":", 1)[0].lower()
        if scheme in ("http", "https"):
             urls.append(url)

    return urls

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")
    return extract_urls(links, base_url)

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    images = soup.find_all("img")
    return extract_urls(images, base_url, "src")