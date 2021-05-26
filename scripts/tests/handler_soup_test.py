from scripts.handler.handler_soup import HandlerSoup
from scripts.requests_server import get_information_webdriver, get_information_requests
from bs4 import BeautifulSoup
import unittest


class MyTestCase(unittest.TestCase):
    url_test = "http://127.0.0.1:5002/"
    delay_error = 0

    def test_find_webdriver(self):
        handler_soup = self.__get_webdriver_handler()

        html_block = handler_soup.find("body")
        info = BeautifulSoup("<html><body>Hello World!</body></html>", 'lxml').find("body")
        self.assertEqual(html_block, info)

        html_block = handler_soup.find("li")
        self.assertNotEqual(html_block, info)

    def test_find_request(self):
        handler_soup = self.__get_request_handler()

        html_block = handler_soup.find("body")
        info = BeautifulSoup("<html><body><p>Hello World!</p></body></html>", 'lxml').find("body")
        self.assertEqual(html_block, info)

    def test_find_all_webdriver(self):
        handler_soup = self.__get_webdriver_handler()

        html_block = handler_soup.find_all("body")
        info = BeautifulSoup("<html><body>Hello World!</body></html>", 'lxml').find_all("body")
        self.assertEqual(html_block, info)

    def test_find_all_request(self):
        handler_soup = self.__get_request_handler()

        html_block = handler_soup.find_all("body")
        info = BeautifulSoup("<html><body><p>Hello World!</p></body></html>", 'lxml').find_all("body")
        self.assertEqual(html_block, info)

        html_block = handler_soup.find("li")
        self.assertNotEqual(html_block, info)

    def __get_webdriver_handler(self):
        webdriver = get_information_webdriver(self.url_test, self.delay_error)
        return HandlerSoup(webdriver)

    def __get_request_handler(self):
        request = get_information_requests(self.url_test, self.delay_error)
        return HandlerSoup(request)


if __name__ == '__main__':
    unittest.main()
