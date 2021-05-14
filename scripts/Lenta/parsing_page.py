""""
    Парсинг страниц магазина лента.
    Страница - https://lenta.com/search/?page=1&searchText=%D0%B3%D1%80%D0%B5%D1%87%D0%BA%D0%B0
"""
import math

from scripts.handler.HandlerSoup import HandlerSoup
from scripts.getting_driver import get_information_requests, get_information_webdriver


class ParsingPageLenta:
    def __init__(self, url, number_start_page, delay_after_error=0):
        self.__url = url
        self.__delay_after_error = delay_after_error
        self.__number_start_page = number_start_page
        self.__max_page = self.__number_start_page + 1
        self.__main_page = "https://lenta.com"

    def get_urls(self):
        # Посмотреть как лучше оформить ловлю ошибки
        soup = get_information_webdriver(url=self.__url + f"&page={self.__number_start_page}",
                                         delay_after_error=self.__delay_after_error)
        self.__get_max_page(soup)
        handler_soup = HandlerSoup(soup)

        block_products = handler_soup.find("div", {"class": "catalog-grid-container__grid"})
        products = block_products.find_all("div", {"class": "sku-card-small-container"})

        for product in products:
            link_product = product.find('a', {"class": "sku-card-small sku-card-small--ecom"})
            print(self.__main_page + link_product.get("href"))

    def __get_max_page(self, soup) -> int:
        # Посмотреть как лучше оформить ловлю ошибки

        number_maximum = -math.inf

        handler_soup = HandlerSoup(soup)
        pagination = handler_soup.find("ul", {"class": "pagination"})
        items = pagination.find_all("li", {"class": "pagination__item"})

        for item in items:
            tag_a = item.find("a")
            number = int(tag_a.text)
            if number > number_maximum:
                number_maximum = number
        return number_maximum


url = "https://lenta.com/search/?searchText=гречка"

if __name__ == '__main__':
    parsing_page_lenta = ParsingPageLenta(url, 1)
    parsing_page_lenta.get_urls()
