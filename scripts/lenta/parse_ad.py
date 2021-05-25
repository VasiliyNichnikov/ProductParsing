"""
    Данный скрипт парсит объявление Leroy Merlin и получает цену, описание товара и сохранение фото.
"""
import os
# import httplib2
# from PIL import Image
from typing import List, Dict
from bs4 import BeautifulSoup
from scripts.errors import TagInformationNotFound
from scripts.handler.handler_soup import HandlerSoup
from scripts.requests_server import get_information_requests, get_information_webdriver


class ParseAd:
    def __init__(self, url, path_images, delay_after_error=0):
        self.url = url
        self.path_images = path_images
        self.soup = get_information_webdriver(url, delay_after_error=delay_after_error)
        self.handler_soup = HandlerSoup()

        print(f"Имя - {self.__get_name()}")
        print(f"Артикул - {self.__get_article_number()}")
        print(f"Цены - {self.__get_default_lenta_card_prices()}")
        self.__get_specifications()
        # print(f"Характеристики - {}")

    # Артикул
    def __get_article_number(self) -> int:
        article_number = 0
        try:
            block_info = self.handler_soup.find(self.soup, "div", {"class": ["sku-page__info"]})
            article = self.handler_soup.find(block_info, "div", {"class": ["sku-page__code-info"]})
            # Сделать проверку на исключения текста
            article_text = article.text
            article_number_text = article_text.split()[-1]
            if article_number_text.isdigit():
                article_number = int(article_number_text)
        except TagInformationNotFound as e:
            print(f"Error - {e}")
        return article_number

    # Название товара
    def __get_name(self) -> str:
        name_text = ""
        try:
            block_header = self.handler_soup.find(self.soup, "div", {"class": ["sku-page__header"]})
            name = self.handler_soup.find(block_header, "h1", {"class": "sku-page__title"})
            name_text = self.__removing_spaces(name.text)
        except TagInformationNotFound as e:
            print(f"Error - {e}")
        return name_text

    def __removing_spaces(self, name_text: str):
        list_words = name_text.split()
        return ' '.join(list_words)

    # Цены в рублях (со скидкой и без)
    def __get_default_lenta_card_prices(self):
        result = {"default": "0.0", "lenta_card": "0.0"}
        try:
            block_main_info = self.handler_soup.find(self.soup, "div",
                                                     {"class": ["sku-page-control-container", "sku-page__control"]})
            block_prices = self.handler_soup.find(block_main_info, "div", {"class": ["sku-prices-block",
                                                                                     "sku-page-control__prices"]})
            default_block_price = self.handler_soup.find(block_prices, "div", {"class": ["sku-price--regular"]})
            lenta_card_block_price = self.handler_soup.find(block_prices, "div", {"class": ["sku-price--primary"]})

            default_price = self.__get_price(default_block_price)
            lenta_card_price = self.__get_price(lenta_card_block_price)
            result = {"default": f"{default_price['integer']}.{default_price['fraction']}",
                      "lenta_card": f"{lenta_card_price['integer']}.{lenta_card_price['fraction']}"}

        except TagInformationNotFound as e:
            print(f"Error - {e}")

        return result

    def __get_price(self, block_price: BeautifulSoup) -> dict:
        integer_number_text = ""
        fraction_number_text = ""
        try:
            integer_number = self.handler_soup.find(block_price, "span", {"class": ["sku-price__integer"]})
            fraction_number = self.handler_soup.find(block_price, "small", {"class": ["sku-price__fraction"]})
            integer_number_text = integer_number.text
            fraction_number_text = fraction_number.text
        except TagInformationNotFound as e:
            print(f"Error - {e}")
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
    parsingAd = ParseAd("https://lenta.com/product/grechka-mistral-fermerskaya-rossiya-900g-479051/", "", 0)
