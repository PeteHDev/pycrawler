import unittest
from crawl import *

class TestCrawl(unittest.TestCase):
    def test_normalize_url1(self):
        input_url = "https://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url2(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url3(self):
        input_url = "http://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url4(self):
        input_url = "http://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

class TestHtmlParsing(unittest.TestCase):
    def test_get_h1_from_html1(self):
        html = "<html><body><h1>Simple Header</h1></body></html>"
        actual = get_h1_from_html(html)
        expected = "Simple Header"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html2(self):
        html = "<html><body><h1>Another Header</h1><h1>Simple Header</h1></body></html>"
        actual = get_h1_from_html(html)
        expected = "Another Header"
        self.assertEqual(actual, expected)

    def test_get_h1_from_html3(self):
        html = "<html><body><h2>Not an h1 header</h2></body></html>"
        actual = get_h1_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_h1_from_html4(self):
        html = '''<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>'''
        actual = get_h1_from_html(html)
        expected = "Welcome to Boot.dev"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html1(self):
        html = '''<html>
        <body>
            <p>First paragraph</p>
            <main>
                <p>First paragraph inside main</p>
                <p>Second paragraph inside main</p>
            </main>
        </body>
        </html>'''
        actual = get_first_paragraph_from_html(html)
        expected = "First paragraph inside main"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html2(self):
        html = '''<html>
        <body>
            <main>
                <p>First paragraph inside main</p>
                <p>Second paragraph inside main</p>
            </main>
            <p>First paragraph</p>
        </body>
        </html>'''
        actual = get_first_paragraph_from_html(html)
        expected = "First paragraph inside main"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html3(self):
        html = '''<html>
        <body>
            <main>
                <h1>Header inside main</h1>
            </main>
        </body>
        </html>'''
        actual = get_first_paragraph_from_html(html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html4(self):
        html = '''<html>
  <body>
    <h1>Welcome to Boot.dev</h1>
    <main>
      <p>Learn to code by building real projects.</p>
      <p>This is the second paragraph.</p>
    </main>
  </body>
</html>'''
        actual = get_first_paragraph_from_html(html)
        expected = "Learn to code by building real projects."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html5(self):
        html = '''<html>
        <body>
            <p>First paragraph no main</p>
            <p>Second paragraph no main</p>
        </body>
        </html>'''
        actual = get_first_paragraph_from_html(html)
        expected = "First paragraph no main"
        self.assertEqual(actual, expected)

class TestUrlsFromHtml(unittest.TestCase):
    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = set(["https://blog.boot.dev"])
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="/somepage.html"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = set(["https://blog.boot.dev/somepage.html"])
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_none(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html>
            <body>
                <p><span>Boot.dev</span></p>
                <a><span>Empty link</span></a>
                <a href=""><span>Empty link again</span></a>
                <a href=" "><span>Empty link again again</span></a>
            </body>
        </html>'''
        actual = get_urls_from_html(input_body, input_url)
        expected = set()
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_mixed(self):
        input_url = "https://blog.boot.dev/"
        input_body = '''<html>
            <body>
                <p>
                    <a href="https://blog.boot.dev"><span>Boot.dev</span></a>
                    <a href="https://blog.boot.dev/absolutepage1.html"><span>Absolute 1</span></a>
                    <a href="/relativepage1.html"><span>Relative 1</span></a>
                    <a href="/relativepage2.html"><span>Relative 2</span></a>
                    <a href="https://blog.boot.dev/absolutepage2.html"><span>Absolute 2</span></a>
                    <a href="https://blog.boot.dev/absolutepage3.html"><span>Absolute 3</span></a>
                    <a href="/relativepage3.html"><span>Relative 3</span></a>
                    <a href="https://google.com"><span>Google:)))</span></a>
                    <a><span>Empty link</span></a>
                    <a href=""><span>Empty link again</span></a>
                    <a href=" "><span>Empty link again again</span></a>
                    <a href="/pagewithaquery?a=1#top"><span>Queried link</span></a>
                </p>
            </body>
        </html>'''
        actual = get_urls_from_html(input_body, input_url)
        expected = set(["https://blog.boot.dev",
                    "https://blog.boot.dev/absolutepage1.html",
                    "https://blog.boot.dev/relativepage1.html",
                    "https://blog.boot.dev/relativepage2.html",
                    "https://blog.boot.dev/absolutepage2.html",
                    "https://blog.boot.dev/absolutepage3.html",
                    "https://blog.boot.dev/relativepage3.html",
                    "https://google.com",
                    "https://blog.boot.dev/pagewithaquery?a=1#top"])
        self.assertEqual(sorted(actual), sorted(expected))

    def test_get_images_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="https://blog.boot.dev/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = set(["https://blog.boot.dev/logo.png"])
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = set(["https://blog.boot.dev/logo.png"])
        self.assertEqual(actual, expected)

    def test_get_images_from_html_none(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html>
            <body>
                <p>Paragraph</p>
                <img alt="No source image">
                <img src="" alt="Empty source image">
                <img src=" " alt="Empty source image again">
                <img src="" alt="Logo 1">
            </body>
        </html>'''
        actual = get_images_from_html(input_body, input_url)
        expected = set()
        self.assertEqual(actual, expected)

    def test_get_images_from_html_mixed(self):
        input_url = "https://blog.boot.dev/"
        input_body = '''
        <html>
            <body>
                <img alt="No source image">
                <img src="" alt="Empty source image">
                <img src=" " alt="Empty source image again">
                <img src="/logo1.png" alt="Logo 1">
                <img src="https://blog.boot.dev/logo2.png" alt="Logo 2">
                <img src="https://picsum.photos/200" alt="Lorem Picsum">
                <img src="https://blog.boot.dev/logo2.png?a=1#top" alt="Queried image">
            </body>
        </html>'''
        actual = get_images_from_html(input_body, input_url)
        expected = set(["https://blog.boot.dev/logo1.png",
                    "https://blog.boot.dev/logo2.png",
                    "https://picsum.photos/200",
                    "https://blog.boot.dev/logo2.png?a=1#top"])
        self.assertEqual(sorted(actual), sorted(expected))

    def test_get_urls_from_html_ignore_non_http(self):
        input_url = "https://blog.boot.dev"
        input_body = '''
        <html><body>
            <a href="mailto:wiz@den">Email</a>
            <a href="javascript:void(0)">JS</a>
            <a href="tel:+123456">Phone</a>
            <a href="https://blog.boot.dev/ok">OK</a>
        </body></html>
        '''
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/ok"]
        self.assertEqual(sorted(actual), sorted(expected))

    def test_get_images_from_html_ignore_data_urls(self):
        input_url = "https://blog.boot.dev"
        input_body = '''
        <html><body>
            <img src="data:image/png;base64,AAAA" alt="inline">
            <img src="https://blog.boot.dev/logo.png" alt="ok">
        </body></html>
        '''
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(sorted(actual), sorted(expected))

    def test_get_urls_from_html_dedup(self):
        input_url = "https://blog.boot.dev"
        input_body = '''
        <html><body>
            <a href="/same.html">One</a>
            <a href="/same.html">Two</a>
        </body></html>
        '''
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/same.html"]
        self.assertEqual(sorted(actual), sorted(expected))

class TestDataExtract(unittest.TestCase):
    def test_extract_page_data_basic(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertDictEqual(actual, expected)

    def test_extract_page_data_nodata(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <spank>Test Title</spank>
            <spank>This is the first paragraph.</spank>
            <spank>Link 1</spank>
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertDictEqual(actual, expected)

    def test_extract_page_data_no_links(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="">Link 1</a>
            <a href=" ">Link 2</a>
            <a href="mailto:wiz@den">Email</a>
            <a href="javascript:void(0)">JS</a>
            <a href="tel:+123456">Phone</a>
            <img src="" alt="Image 1">
            <img src=" " alt="Image 2">
            <img src="data:image/png;base64,AAAA" alt="inline">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertDictEqual(actual, expected)

    def test_extract_page_data_mixed(self):
        input_url = "https://blog.boot.dev/"
        input_body = '''
        <html>
            <body>
                <h1>TITLE!!!</h1>
                <p>Wrong first paragraph</p>
                <main>
                    <p>Correct first paragraph</p>
                </main>
                <a href="https://blog.boot.dev"><span>Boot.dev</span></a>
                <a href="https://blog.boot.dev/absolutepage1.html"><span>Absolute 1</span></a>
                <a href="/relativepage1.html"><span>Relative 1</span></a>
                <a href="/relativepage2.html"><span>Relative 2</span></a>
                <a href="https://blog.boot.dev/absolutepage2.html"><span>Absolute 2</span></a>
                <a href="https://blog.boot.dev/absolutepage3.html"><span>Absolute 3</span></a>
                <a href="/relativepage3.html"><span>Relative 3</span></a>
                <a href="https://google.com"><span>Google:)))</span></a>
                <a><span>Empty link</span></a>
                <a href=""><span>Empty link again</span></a>
                <a href=" "><span>Empty link again again</span></a>
                <a href="/pagewithaquery?a=1#top"><span>Queried link</span></a>
                <a href="mailto:wiz@den">Email</a>
                <a href="javascript:void(0)">JS</a>
                <a href="tel:+123456">Phone</a>
                <img alt="No source image">
                <img src="" alt="Empty source image">
                <img src=" " alt="Empty source image again">
                <img src="data:image/png;base64,AAAA" alt="inline">
                <img src="/logo1.png" alt="Logo 1">
                <img src="https://blog.boot.dev/logo2.png" alt="Logo 2">
                <img src="https://picsum.photos/200" alt="Lorem Picsum">
                <img src="https://blog.boot.dev/logo2.png?a=1#top" alt="Queried image">
            </body>
        </html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "TITLE!!!",
            "first_paragraph": "Correct first paragraph",
            "outgoing_links": sorted([
                    "https://blog.boot.dev",
                    "https://blog.boot.dev/absolutepage1.html",
                    "https://blog.boot.dev/relativepage1.html",
                    "https://blog.boot.dev/relativepage2.html",
                    "https://blog.boot.dev/absolutepage2.html",
                    "https://blog.boot.dev/absolutepage3.html",
                    "https://blog.boot.dev/relativepage3.html",
                    "https://google.com",
                    "https://blog.boot.dev/pagewithaquery?a=1#top"]),
            "image_urls": sorted([
                    "https://blog.boot.dev/logo1.png",
                    "https://blog.boot.dev/logo2.png",
                    "https://picsum.photos/200",
                    "https://blog.boot.dev/logo2.png?a=1#top"])
        }
        self.assertDictEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()

"""
https://blog.boot.dev/path/
https://blog.boot.dev/path
http://blog.boot.dev/path/
http://blog.boot.dev/path
blog.boot.dev/path
"""