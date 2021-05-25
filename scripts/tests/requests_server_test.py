import unittest
from bs4 import BeautifulSoup
from scripts.requests_server import get_information_requests, get_information_webdriver


class RequestsServerTest(unittest.TestCase):
    url_test = "http://127.0.0.1:5002/"
    delay_error = 0

    def test_information_requests(self):
        func = get_information_requests
        info = BeautifulSoup("<html><body><p>Hello World!</p></body></html>", 'lxml')
        self.assertEqual(func(self.url_test, self.delay_error), info)

    def test_information_webdriver(self):
        func = get_information_webdriver
        info = BeautifulSoup("<html><head></head><body>Hello World!</body></html>", 'lxml')
        self.assertEqual(func(self.url_test, self.delay_error), info)


if __name__ == '__main__':
    unittest.main()
