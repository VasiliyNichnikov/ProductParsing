""""
    Парсинг страниц магазина лента.
    Страница - https://lenta.com/search/?page=1&searchText=%D0%B3%D1%80%D0%B5%D1%87%D0%BA%D0%B0
"""
import math
import typing
from scripts.handler.HandlerSoup import HandlerSoup
from scripts.Errors import TagInformationNotFound
from scripts.GettingDriver import get_information_webdriver


class ParsingPage:
    def __init__(self, url, number_start_page, delay_after_error=0):
        self.__url = url
        self.__delay_after_error = delay_after_error
        self.__number_start_page = number_start_page
        self.__max_page = self.__number_start_page + 1
        self.__main_page = "https://lenta.com"

    def get_urls(self):
        list_urls = []
        # Посмотреть как лучше оформить ловлю ошибки
        soup = get_information_webdriver(url=self.__url + f"&page={self.__number_start_page}",
                                         delay_after_error=self.__delay_after_error)
        print(self.__get_max_page(soup))
        try:
            products = self.__get_products(soup)
            for product in products:
                link_product = product.find('a', {"class": "sku-card-small sku-card-small--ecom"})
                url = self.__main_page + link_product.get("href")
                list_urls.append(url)
        except TagInformationNotFound as e:
            print(f"Error - {e}")
        return list_urls

    @staticmethod
    def __get_products(soup) -> typing.List[HandlerSoup]:
        handler_soup = HandlerSoup(soup)

        block_products = handler_soup.find("div", {"class": "catalog-grid-container__grid"})
        products = block_products.find_all("div", {"class": "sku-card-small-container"})
        return products

    def __get_max_page(self, soup) -> int:
        # Посмотреть как лучше оформить ловлю ошибки

        number_maximum = -math.inf
        try:
            items = self.__get_items(soup)

            for item in items:
                number_maximum = self.__get_number_maximum(item, number_maximum)
        except TagInformationNotFound as e:
            print(f"Error - {e}")
        return number_maximum

    @staticmethod
    def __get_items(soup) -> typing.List[HandlerSoup]:
        handler_soup = HandlerSoup(soup)
        pagination = handler_soup.find("ul", {"class": "pagination"})
        items = pagination.find_all("li", {"class": "pagination__item"})
        return items

    @staticmethod
    def __get_number_maximum(item, number_maximum):
        tag_a = item.find("a")
        number = int(tag_a.text)
        if number > number_maximum:
            number_maximum = number
        return number_maximum


test_url = "https://lenta.com/search/?searchText=гречка"

if __name__ == '__main__':
    parsing_page_lenta = ParsingPage(test_url, 1)
    print(parsing_page_lenta.get_urls())
