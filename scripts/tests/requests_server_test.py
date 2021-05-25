import unittest
from bs4 import BeautifulSoup
from scripts.requests_server import get_information_requests, get_information_webdriver


class RequestsServerTest(unittest.TestCase):
    url_test = "https://www.test.com"
    delay_error = 0

    def test_information_requests(self):
        info = ""
        with open("test_html.html", "r", encoding="utf-8") as read:
            info = read.read()
        # print(info)
        func = get_information_requests
        self.assertEqual(func(self.url_test, self.delay_error), info)

    def test_information_webdriver(self):
        pass
        # func = get_information_webdriver
        # self.assertEqual(func(self.url_test, self.delay_error), BeautifulSoup)


if __name__ == '__main__':
    unittest.main()
