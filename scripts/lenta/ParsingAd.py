"""
    Данный скрипт парсит объявление Leroy Merlin и получает цену, описание товара и сохранение фото.
"""
import os
# import httplib2
# from PIL import Image
from bs4 import BeautifulSoup
from scripts.Errors import TagInformationNotFound
from scripts.handler.HandlerSoup import HandlerSoup
from scripts.GettingDriver import get_information_requests, get_information_webdriver


class ParsingAd:
    def __init__(self, url, path_images, delay_after_error=0):
        self.url = url
        self.path_images = path_images
        self.soup = get_information_webdriver(url, delay_after_error=delay_after_error)
        self.handler_soup = HandlerSoup(self.soup)

        print(f"Имя - {self.__get_name()}")
        print(f"Артикул - {self.__get_article_number()}")
        print(f"Цены - {self.__get_default_lenta_card_prices()}")

    # Артикул
    def __get_article_number(self) -> int:
        article_number = 0
        try:
            block_info = self.handler_soup.find("div", {"class": ["sku-page__info"]})
            article = block_info.find("div", {"class": ["sku-page__code-info"]})
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
            block_header = self.handler_soup.find("div", {"class": ["sku-page__header"]})
            name = block_header.find("h1", {"class": "sku-page__title"})
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
            block_main_info = self.handler_soup.find("div",
                                                     {"class": ["sku-page-control-container", "sku-page__control"]})
            block_prices = block_main_info.find("div", {"class": ["sku-prices-block", "sku-page-control__prices"]})
            default_block_price = block_prices.find("div", {"class": ["sku-price--regular"]})
            lenta_card_block_price = block_prices.find("div", {"class": ["sku-price--primary"]})

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
            integer_number = block_price.find("span", {"class": ["sku-price__integer"]})
            fraction_number = block_price.find("small", {"class": ["sku-price__fraction"]})
            integer_number_text = integer_number.text
            fraction_number_text = fraction_number.text
        except TagInformationNotFound as e:
            print(f"Error - {e}")
        return {"integer": integer_number_text, "fraction": fraction_number_text}

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

    # # Возвращает название товара
    # def __get_name(self):
    #     dict_result = {'name': '0'}
    #     name = self.soup.find('h1', {'slot': 'title', 'itemprop': 'name', 'class': 'header-2'})
    #     if name is not None:
    #         dict_result['name'] = name.text
    #     return dict_result['name']
    #
    # # Возвращает цену товара
    # def __get_price(self):
    #     dict_result = {'price': '0'}
    #     block_price = self.soup.find('uc-pdp-price-view',
    #                                  {'slot': 'primary-price', 'class': 'primary-price', 'itemprop': 'offers'})
    #     if block_price is not None:
    #         price = block_price.find('span', {'slot': 'price'})
    #         if price is not None:
    #             dict_result['price'] = price.text
    #     return dict_result['price']
    #
    # # Возвращает кол-во товара
    # def __get_quantity_goods(self):
    #     dict_result = {'quantity_goods': '0'}
    #     block_goods = self.soup.find('uc-elbrus-pdp-stocks-list', {'slot': 'extra-info', 'stocksource': 'STEP'})
    #     if block_goods is not None:
    #         list_goods = block_goods.find_all('uc-store-stock')
    #         if list_goods is not None:
    #             list_result = []
    #             for product in list_goods:
    #                 shop = product.find('span').text
    #                 number = product.get('stock')
    #                 list_result.append(f'{shop}:{number}')
    #             dict_result['quantity_goods'] = self.__translate_list_to_string(list_result)
    #     return dict_result['quantity_goods']
    #
    # # Перевод в граммы
    # def __conversion_to_grams(self, number):
    #     return float(number) * 1000
    #
    # # Перевод в миллиметры
    # def __conversion_millimeters(self, number):
    #     return float(number) * 1000
    #
    # # Получение характеристик
    # def __get_specifications(self):
    #     block_specifications = self.soup.find('dl', {'class': 'def-list'})
    #     dict_result = {'вес': '0', 'ширина': '0', 'высота': '0',
    #                    'модель': '0', 'тип': '0', 'марка': '0', 'изготовитель': '0', 'объем': '0', 'другое': []}
    #     if block_specifications is not None:
    #         list_items = block_specifications.find_all('div', {'class': 'def-list__group'})
    #
    #         if list_items is not None:
    #             list_other = []
    #             for item in list_items:
    #                 key_save = item.find('dt', {'class': 'def-list__term'}).text.replace('\n', '')
    #                 key = key_save.replace(' ', '').lower()
    #                 value = item.find('dd', {'class': 'def-list__definition'}).text.replace('\n', '') \
    #                     .replace('                ', '').lower()
    #
    #                 if 'вес,кг' in key:
    #                     dict_result['вес'] = self.__conversion_to_grams(value.replace(' ', ''))
    #                 elif 'ширинатоваравиндивидуальнойупаковке' in key:
    #                     dict_result['ширина'] = self.__conversion_millimeters(value.replace(' ', ''))
    #                 elif 'высотатоваравиндивидуальнойупаковке' in key:
    #                     dict_result['высота'] = self.__conversion_millimeters(value.replace(' ', ''))
    #                 elif 'модельпродукта' in key:
    #                     dict_result['модель'] = value
    #                 elif 'типпродукта' in key:
    #                     dict_result['тип'] = value
    #                 elif 'марка' in key:
    #                     dict_result['марка'] = value
    #                 elif 'странапроизводства' in key:
    #                     dict_result['изготовитель'] = value
    #                 elif 'объем(л)' in key:
    #                     dict_result['объем'] = value.replace(' ', '')
    #                 else:
    #                     list_other.append(f'{key_save}:{value}')
    #             dict_result['другое'] = self.__translate_list_to_string(list_other)
    #     return dict_result
    #
    # # Установка изображений
    # def __save_images(self, list_images):
    #     list_images_path = []
    #     ready_path = self.path_images + f'/{self.__get_name()}'
    #     try:
    #         # Создание папки
    #         os.mkdir(ready_path)
    #         # Добавление изображений в папку
    #         h = httplib2.Http('.cache')
    #         number = 0
    #         for image in list_images:
    #             number += 1
    #             response, content = h.request(image)
    #             image_path = ready_path + f'/{number}.png'
    #             out = open(image_path, 'wb')
    #             out.write(content)
    #             out.close()
    #             self.__changing_image(image_path)
    #             if image_path is not None:
    #                 list_images_path.append(os.path.abspath(image_path))
    #         return list_images_path
    #     except OSError:
    #         print('Создать директорию %s не удалось' % ready_path)
    #     return None
    #
    # # Изменение размера изображения
    # def __changing_image(self, image):
    #     original_image = Image.open(image)
    #     width, height = original_image.size
    #     size = (1600, 700)
    #     if width == height:
    #         size = (700, 700)
    #     resized_image = original_image.resize(size)
    #     resized_image.save(image)
    #
    # # Получение описания
    # def __get_description(self):
    #     dict_result = {'description': '0'}
    #     block_description = self.soup.find('section', {'class': ['pdp-section', 'pdp-section--product-description'],
    #                                                    'id': 'nav-description'})
    #     if block_description is not None:
    #         description = block_description.find('div').text.replace('\n', ' ')
    #         dict_result['description'] = description
    #     return dict_result['description']
    #
    # # Получение артикля фото
    # def __get_article_photo(self, list_photos):
    #     return [photo.split('/')[-1][:-4] for photo in list_photos]
    #
    # # Получение всех фото товара
    # def __get_all_photos_product(self):
    #     dict_result = {'main-photo': '', 'additional-photos': '0', 'photo-articles': '0'}
    #     block_photos = self.soup.find('uc-pdp-media-carousel', {'slot': 'media-content'})
    #     list_result = []
    #     if block_photos is not None:
    #         list_photos = block_photos.find_all('picture', {'slot': 'pictures'})
    #         if list_photos is not None:
    #             for photo in list_photos:
    #                 photo = photo.find('source', {'itemprop': 'image'})
    #                 list_result.append(photo.get('srcset'))
    #     if len(list_result) != 0 and list_result is not None:
    #         list_images_path = self.__save_images(list_result)
    #         if list_images_path is not None:
    #             dict_result['main-photo'] = self.__translate_list_to_string(list_images_path[0:2])
    #             if len(list_images_path) > 2:
    #                 dict_result['additional-photos'] = self.__translate_list_to_string(list_images_path[2:])
    #             dict_result['photo-articles'] = self.__translate_list_to_string(self.__get_article_photo(list_result))
    #     else:
    #         print('Фото не найдены')
    #     return dict_result
    #
    # # Перевод списка в строку
    # def __translate_list_to_string(self, _list):
    #     result = ''
    #     for item in _list:
    #         result += item + '\n'
    #     return result
    #
    # # Получение всей собранной инфомармации
    # def get_info(self):
    #     name = self.__get_name()
    #     price = self.__get_price()
    #
    #     specifications = self.__get_specifications()
    #     weight = specifications['вес']
    #     width = specifications['ширина']
    #     height = specifications['высота']
    #     model = specifications['модель']
    #     type_model = specifications['тип']
    #     brand = specifications['марка']
    #     manufacturer = specifications['изготовитель']
    #     volume = specifications['объем']
    #     other = specifications['другое']
    #
    #     all_photos = self.__get_all_photos_product()
    #     main_photo = all_photos['main-photo']
    #     additional_photos = all_photos['additional-photos']
    #     photo_articles = all_photos['photo-articles']
    #
    #     description = self.__get_description()
    #     quantity_goods = self.__get_quantity_goods()
    #
    #     return {
    #         'NAME': name,
    #         'PRICE': price,
    #         'WEIGHT': weight,
    #         'WIDTH': width,
    #         'HEIGHT': height,
    #         'MODEL': model,
    #         'TYPE_MODEL': type_model,
    #         'BRAND': brand,
    #         'MANUFACTURER': manufacturer,
    #         'VOLUME': volume,
    #         'MAIN_PHOTO': main_photo,
    #         'ADDITIONAL_PHOTOS': additional_photos,
    #         'PHOTO_ARTICLES': photo_articles,
    #         'DESCRIPTION': description,
    #         'QUANTITY_GOODS': quantity_goods,
    #         'OTHER': other,
    #         'URL': self.url
    #     }


if __name__ == "__main__":
    parsingAd = ParsingAd("https://lenta.com/product/grechka-mistral-fermerskaya-rossiya-900g-479051/", "", 0)
