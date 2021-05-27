"""
    Данный скрипт парсит объявление Leroy Merlin и получает цену, описание товара и сохранение фото.
"""
import os
# import httplib2
# from PIL import Image
from typing import List, Dict
from bs4 import BeautifulSoup, PageElement, ResultSet
from scripts.errors import TagInformationNotFound, TextTagNotFound
from scripts.handler.handler_soup import HandlerSoup, HandlerSoup2
from scripts.requests_server import get_information_requests, get_information_webdriver


class ParseAd:
    def __init__(self, url, path_images, delay_after_error=0):
        self.url = url
        self.path_images = path_images
        self.soup = get_information_webdriver(url, delay_after_error=delay_after_error)
        self.handler_soup = HandlerSoup2(self.soup)

        # print(f"Имя - {self.__get_name()}")
        # print(f"Артикул - {self.__get_article_number()}")
        # print(f"Цены - {self.__get_default_lenta_card_prices()}")

    # Артикул
    def __get_article_number(self) -> int:
        self.handler_soup.soup = self.soup
        article_number = 0

        page_info = self.handler_soup.find("div", {"class": ["sku-page__info"]})
        self.handler_soup.soup = page_info
        page_code = self.handler_soup.find("div", {"class": ["sku-page__code-info"]})
        self.handler_soup.soup = page_code

        article_text = self.handler_soup.text
        # article_text = page_code.

        article_split = article_text.split()
        if len(article_split) != 0 and article_split[-1].isdigit():
            article_number = int(article_split[-1])

        return article_number

    # Название товара
    def __get_name(self) -> str:
        self.handler_soup.soup = self.soup

        page_header = self.handler_soup.find("div", {"class": ["sku-page__header"]})
        self.handler_soup.soup = page_header

        page_title = self.handler_soup.find("h1", {"class": "sku-page__title"})
        self.handler_soup.soup = page_title

        name_text = self.__removing_spaces(self.handler_soup.text)
        return name_text

    def __removing_spaces(self, name_text: str):
        list_words = name_text.split()
        return ' '.join(list_words)

    # Цены в рублях (со скидкой и без)
    def __get_default_lenta_card_prices(self):
        self.handler_soup.soup = self.soup
        page_control_container = self.handler_soup.find("div",
                                                        {"class": ["sku-page-control-container", "sku-page__control"]})
        self.handler_soup.soup = page_control_container
        prices_block = self.handler_soup.find("div", {"class": ["sku-prices-block",
                                                                "sku-page-control__prices"]})

        self.handler_soup.soup = prices_block
        default_block_price = self.handler_soup.find("div", {"class": ["sku-price--regular"]})
        lenta_card_block_price = self.handler_soup.find("div", {"class": ["sku-price--primary"]})

        default_price = self.__get_price(default_block_price)
        lenta_card_price = self.__get_price(lenta_card_block_price)

        result = {"default": f"{default_price['integer']}.{default_price['fraction']}",
                  "lenta_card": f"{lenta_card_price['integer']}.{lenta_card_price['fraction']}"}
        return result

    def __get_price(self, block_price: [BeautifulSoup, PageElement, ResultSet]) -> dict:
        self.handler_soup.soup = block_price

        integer_number = self.handler_soup.find("span", {"class": ["sku-price__integer"]})
        fraction_number = self.handler_soup.find("small", {"class": ["sku-price__fraction"]})

        self.handler_soup.soup = integer_number
        integer_number_text = self.handler_soup.text

        self.handler_soup.soup = fraction_number
        fraction_number_text = self.handler_soup.text
        return {"integer": integer_number_text, "fraction": fraction_number_text}

    def __get_specifications(self):
        block_specifications = self.handler_soup.find(self.soup, "div", {"class": ["sku-card-tab__content-item",
                                                                                   "sku-card-tab__content-item--active"]})
        block_group = self.handler_soup.find(block_specifications, "div", {"class": ["sku-card-tab-params__group"]})
        print(self.__get_items_specifications(block_group))

    def __get_items_specifications(self, block_group: BeautifulSoup) -> List[Dict[str, str]]:
        specifications_items = []

        items = self.handler_soup.find_all(block_group, "div", {"class": "sku-card-tab-params__item"})
        for item in items:
            label = self.handler_soup.find(item, "label", {"class": ["sku-card-tab-params__label"]})
            info = self.handler_soup.find(item, "a", {"class": ["link sku-card-tab-params__link"]})
            if info is None:
                info = item.find("dd", {"class": ["sku-card-tab-params__value"]})
            label_text = self.__removing_spaces(label.text)
            info_text = self.__removing_spaces(info.text)

            specifications = {"label": label_text, "info": info_text}
            specifications_items.append(specifications)
        return specifications_items

    # Вес в упаковке (г)
    # Ширина упаковки (мм)
    # Высота упаковки (мм).
    # Длина упаковки (мм)
    # Ссылка на главное фото
    # Ссылка на доп.фото
    # Ссылка на фото 360
    # Ссылка на фото аннотаций
    # Артикул фото
    # Название модели
    # Тип
    # Вес товара (г)
    # Состав
    # Условие хранения
    # Срок годности (в днях)
    # Бренд
    # Единиц в одном товаре
    # Описание
    # Страна изготовитель


if __name__ == "__main__":
    parsing_ad = ParseAd("https://lenta.com/product/grechka-mistral-fermerskaya-rossiya-900g-479051/", "", 0)
