from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_error(error_msg):
    if not error_msg is str:
        error_msg = str(error_msg)
    print(bcolors.FAIL + error_msg + bcolors.ENDC)

def print_warning(warning_msg):
    print(bcolors.WARNING + warning_msg + bcolors.ENDC)

def print_list(list):
    for item in list:
        print(item)

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
    urls = set()
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
             urls.add(url)

    return urls

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a")
    return extract_urls(links, base_url)

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    images = soup.find_all("img")
    return extract_urls(images, base_url, "src")

def extract_page_data(html, page_url):
    extracted_data = {}
    extracted_data["url"] = page_url.rstrip("/")
    extracted_data["h1"] = get_h1_from_html(html)
    extracted_data["first_paragraph"] = get_first_paragraph_from_html(html)
    extracted_data["outgoing_links"] = sorted(get_urls_from_html(html, page_url))
    extracted_data["image_urls"] = sorted(get_images_from_html(html, page_url))
    return extracted_data

def get_html(url):
    response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"}, timeout=7)
    response.raise_for_status()
    content_type = response.headers.get("Content-Type", "")
    if not content_type:
        raise Exception(f"{url} has Content-Type header missing")
    elif not "text/html" in content_type.lower():
        raise TypeError("Content-type is not text/html")
    
    return response.text

def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url
    else:
        base_parsed = urlparse(base_url)
        current_parsed = urlparse(current_url)
        if base_parsed.hostname != current_parsed.hostname:
            return
        
    if page_data is None:
        page_data = {}
        
    current_normalized = normalize_url(current_url)
    if current_normalized in page_data:
        return
    
    html = None
    try:
        html = get_html(current_url)
    except TypeError as te:
        print_error(te)
        page_data[current_normalized] = "No text/html"
        return
    except Exception as e:
        print_error(e)
        page_data[current_normalized] = "Something went wrong"
        return
    
    print("Crawling " + current_url + "(" + current_normalized + ")")
    data = extract_page_data(html, current_url)
    page_data[current_normalized] = data
    for link in data["outgoing_links"]:
        crawl_page(base_url, link, page_data)

    return page_data

