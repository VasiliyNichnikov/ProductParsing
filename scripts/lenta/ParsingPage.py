""""
    Парсинг страниц магазина лента.
    Страница - https://lenta.com/search/?page=1&searchText=%D0%B3%D1%80%D0%B5%D1%87%D0%BA%D0%B0
"""
import math
from typing import List
from bs4 import BeautifulSoup

from scripts.handler.HandlerSoup import HandlerSoup
from scripts.Errors import TagInformationNotFound
from scripts.GettingDriver import get_information_webdriver


class ParsingPageLenta:
    def __init__(self, url, number_start_page, delay_after_error=0):
        self.__url = url
        self.__delay_after_error = delay_after_error
        self.__number_now_page = number_start_page
        self.__max_page = self.__number_now_page + 1
        self.__main_page = "https://lenta.com"

    def get_urls(self):
        soup = get_information_webdriver(url=self.__url + f"&page={self.__number_now_page}",
                                         delay_after_error=self.__delay_after_error)
        handler_soup = HandlerSoup(soup)
        products = self.__get_products(handler_soup)

        for product in products:
            link_product = product.find('a', {"class": "sku-card-small sku-card-small--ecom"})
            print(self.__main_page + link_product.get("href"))

    def __get_products(self, handler_soup) -> List[BeautifulSoup]:
        products = []
        try:
            block_products = handler_soup.find("div", {"class": "catalog-grid-container__grid"})
            products = block_products.find_all("div", {"class": "sku-card-small-container"})
        except TagInformationNotFound as e:
            print("Error - %s" % e)
        return products

    def __get_max_page(self, soup) -> int:
        number_maximum = -math.inf

        handler_soup = HandlerSoup(soup)
        items = self.__get_items(handler_soup)

        for item in items:
            number_maximum = self.__search_max_number(item, number_maximum)
        return int(number_maximum)

    def __get_items(self, handler_soup) -> List[BeautifulSoup]:
        items = []
        try:
            pagination = handler_soup.find("ul", {"class": "pagination"})
            items = pagination.find_all("li", {"class": "pagination__item"})
        except TagInformationNotFound as e:
            print("Error - %s" % e)
        return items

    def __search_max_number(self, item: BeautifulSoup, number_maximum: float) -> float:
        tag_a = item.find('a')
        text_a = tag_a.text
        if text_a.isdigit():
            number_a = int(text_a)
            if number_a > number_maximum:
                number_maximum = number_a
        return number_maximum


url = "https://lenta.com/search/?searchText=гречка"

if __name__ == '__main__':
    parsing_page_lenta = ParsingPageLenta(url, 1)
    parsing_page_lenta.get_urls()
