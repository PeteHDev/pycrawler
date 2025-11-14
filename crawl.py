from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests
import asyncio
import aiohttp

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
    base_parsed = urlparse(base_url)
    for link in links:
        val = link.get(look_for)
        if not val:
            continue

        ref = link.get(look_for).strip()
        if not ref:
            continue

        url = urljoin(base_url, ref)
        url_parsed = urlparse(url)
        if url_parsed.netloc != base_parsed.netloc:
            continue

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

class AsyncCrawler:
    def __init__(self, base_url, max_pages=100, max_concurrency=3):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.max_pages = max_pages
        self.max_concurrency = max_concurrency
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
        self.should_stop = False
        self.all_tasks = set()

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop:
                return False
            if normalized_url in self.page_data:
                return False
            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print_warning("Reached maximum number of pages to crawl")
                for task in self.all_tasks:
                    if not task.done():
                        task.cancel()
                return False
            self.page_data[normalized_url] = "dummy data"
            return True
        
    async def get_html(self, url):
        try:
            async with self.session.get(
                url, headers={"User-Agent": "BootCrawler/1.0"}
            ) as response:
                if response.status > 399:
                    print(f"Error: HTTP {response.status} for {url}")
                    return None

                content_type = response.headers.get("content-type", "")
                if "text/html" not in content_type:
                    print_error(f"Error: Non-HTML content {content_type} for {url}")
                    return None

                return await response.text()
        except Exception as e:
            print_error(f"Error fetching {url}: {e}")
            return None
        
    async def crawl_page(self, current_url):
        if self.should_stop:
            return
        
        current_url_obj = urlparse(current_url)
        if current_url_obj.netloc != self.base_domain:
            return

        normalized_url = normalize_url(current_url)

        is_new = await self.add_page_visit(normalized_url)
        if not is_new:
            return

        async with self.semaphore:
            html = await self.get_html(current_url)
            if html is None:
                async with self.lock:
                    self.page_data[normalized_url] = "No HTML"
                    return

            print(f"Crawling {current_url} (Active: {self.max_concurrency - self.semaphore._value})")
            page_info = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized_url] = page_info

            next_urls = get_urls_from_html(html, current_url)

        tasks = []
        for next_url in next_urls:
            tasks.append(asyncio.create_task(self.crawl_page(next_url)))

        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            finally:
                for task in tasks:
                    self.all_tasks.discard(task)
    
    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data
    