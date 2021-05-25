from scripts.handler.handler_soup import HandlerSoup
from scripts.requests_server import get_information_webdriver, get_information_requests
from bs4 import BeautifulSoup
import unittest


class MyTestCase(unittest.TestCase):
    url_test = "http://127.0.0.1:5002/"
    delay_error = 0

    def setUp(self) -> None:
        self.soup_webdriver = get_information_webdriver(self.url_test, self.delay_error)
        self.soup_requests = get_information_requests(self.url_test, self.delay_error)

        self.handler_soup = HandlerSoup()

    def test_find_webdriver(self):
        html_block = self.handler_soup.find(self.soup_webdriver, "body")
        info = BeautifulSoup("<html><body>Hello World!</body></html>", 'lxml').find("body")
        self.assertEqual(html_block, info)

    def test_find_request(self):
        html_block = self.handler_soup.find(self.soup_requests, "body")
        info = BeautifulSoup("<html><body><p>Hello World!</p></body></html>", 'lxml').find("body")
        self.assertEqual(html_block, info)

    def test_find_all_webdriver(self):
        html_block = self.handler_soup.find_all(self.soup_webdriver, "body")
        info = BeautifulSoup("<html><body>Hello World!</body></html>", 'lxml').find_all("body")
        self.assertEqual(html_block, info)

    def test_find_all_request(self):
        html_block = self.handler_soup.find_all(self.soup_requests, "body")
        info = BeautifulSoup("<html><body><p>Hello World!</p></body></html>", 'lxml').find_all("body")
        self.assertEqual(html_block, info)


    # def test_find_all(self):
    #     pass


if __name__ == '__main__':
    unittest.main()
