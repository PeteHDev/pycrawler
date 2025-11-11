import unittest
from crawl import normalize_url, get_h1_from_html, get_first_paragraph_from_html

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


if __name__ == "__main__":
    unittest.main()

"""
https://blog.boot.dev/path/
https://blog.boot.dev/path
http://blog.boot.dev/path/
http://blog.boot.dev/path
blog.boot.dev/path
"""