"""
    Данный скрипт парсит объявление Leroy Merlin и получает цену, описание товара и сохранение фото.
"""

from scripts.GettingDriver import get_information


class ParsingAd:
    def __init__(self, url, delay_after_error=0):
        self.url = url
        self.soup = get_information(url, delay_after_error=delay_after_error)

    # Возвращает название товара
    def __get_name(self):
        dict_result = {'name': '0'}
        name = self.soup.find('h1', {'slot': 'title', 'itemprop': 'name', 'class': 'header-2'})
        if name is not None:
            dict_result['name'] = name.text
        return dict_result['name']

    # Возвращает цену товара
    def __get_price(self):
        dict_result = {'price': '0'}
        block_price = self.soup.find('uc-pdp-price-view',
                                     {'slot': 'primary-price', 'class': 'primary-price', 'itemprop': 'offers'})
        if block_price is not None:
            price = block_price.find('span', {'slot': 'price'})
            if price is not None:
                dict_result['price'] = price.text
        return dict_result['price']

    # Возвращает кол-во товара
    def __get_quantity_goods(self):
        dict_result = {'quantity_goods': '0'}
        block_goods = self.soup.find('uc-elbrus-pdp-stocks-list', {'slot': 'extra-info', 'stocksource': 'STEP'})
        if block_goods is not None:
            list_goods = block_goods.find_all('uc-store-stock')
            if list_goods is not None:
                list_result = []
                for product in list_goods:
                    shop = product.find('span').text
                    number = product.get('stock')
                    list_result.append(f'{shop}:{number}')
                dict_result['quantity_goods'] = self.__translate_list_to_string(list_result)
        return dict_result['quantity_goods']

    # Перевод в граммы
    def __conversion_to_grams(self, number):
        return float(number) * 1000

    # Перевод в миллиметры
    def __conversion_millimeters(self, number):
        return float(number) * 1000

    # Получение характеристик
    def __get_specifications(self):
        block_specifications = self.soup.find('dl', {'class': 'def-list'})
        dict_result = {'вес': '0', 'ширина': '0', 'высота': '0',
                       'модель': '0', 'тип': '0', 'марка': '0', 'изготовитель': '0', 'объем': '0'}
        if block_specifications is not None:
            list_items = block_specifications.find_all('div', {'class': 'def-list__group'})

            if list_items is not None:
                for item in list_items:
                    key = item.find('dt', {'class': 'def-list__term'}).text.replace('\n', '').replace(' ', '').lower()
                    value = item.find('dd', {'class': 'def-list__definition'}).text.replace('\n', '')\
                        .replace('                ', '').lower()

                    if 'вес,кг' in key:
                        dict_result['вес'] = self.__conversion_to_grams(value.replace(' ', ''))
                        # print(f'Вес - {value}')
                    elif 'ширинатоваравиндивидуальнойупаковке' in key:
                        dict_result['ширина'] = self.__conversion_millimeters(value.replace(' ', ''))
                        # print(f'Ширина - {value}')
                    elif 'высотатоваравиндивидуальнойупаковке' in key:
                        dict_result['высота'] = self.__conversion_millimeters(value.replace(' ', ''))
                        # print(f'Высота - {value}')
                    elif 'модельпродукта' in key:
                        dict_result['модель'] = value
                        # print(f'Модель - {value}')
                    elif 'типпродукта' in key:
                        dict_result['тип'] = value
                        # print(f'Тип - {value}')
                    elif 'марка' in key:
                        dict_result['марка'] = value
                        # print(f'Марка - {value}')
                    elif 'странапроизводства' in key:
                        dict_result['изготовитель'] = value
                        # print(f'Страна изготовитель - {value}')
                    elif 'объем(л)' in key:
                        dict_result['объем'] = value.replace(' ', '')
                        # print(f'Объем,л - {value}')
                    # else:
                    #     print(f'Не определен; Key - {key}; Value - {value}')
        return dict_result

    # Получение описания
    def __get_description(self):
        dict_result = {'description': '0'}
        block_description = self.soup.find('section', {'class': ['pdp-section', 'pdp-section--product-description'],
                                                       'id': 'nav-description'})
        if block_description is not None:
            description = block_description.find('div').text.replace('\n', ' ')
            dict_result['description'] = description
        return dict_result['description']

    # Получение артикля фото
    def __get_article_photo(self, list_photos):
        return [photo.split('/')[-1][:-4] for photo in list_photos]

    # Получение всех фото товара
    def __get_all_photos_product(self):
        dict_result = {'main-photo': '', 'additional-photos': '0', 'photo-articles': '0'}
        block_photos = self.soup.find('uc-pdp-media-carousel', {'slot': 'media-content'})
        list_result = []
        if block_photos is not None:
            list_photos = block_photos.find_all('picture', {'slot': 'pictures'})
            if list_photos is not None:
                for photo in list_photos:
                    photo = photo.find('source', {'itemprop': 'image'})
                    list_result.append(photo.get('srcset'))
        if len(list_result) != 0 and list_result is not None:
            dict_result['main-photo'] = list_result[0]
            if len(list_result) > 1:
                dict_result['additional-photos'] = self.__translate_list_to_string(list_result[1:])  # Может произойти ошибка, если будет только одно фото
            dict_result['photo-articles'] = self.__translate_list_to_string(self.__get_article_photo(list_result))
        else:
            print('Фото не найдены')
        return dict_result

    # Получение ссылки на главное фото
    # def __get_url_main_photo(self):
    #     block_url_main_photo = self.soup.find('picture', {'slot': 'pictures', 'id': 'picture-box-id-generated-6',
    #                                                       'aria-labeledby': 'thumb-box-id-generated-6'})
    #     if block_url_main_photo is not None:
    #         url_main_photo = block_url_main_photo.find('source', {'media': ' only screen and (min-width: 1024px)',
    #                                                               'itemprop': 'image'})
    #         if url_main_photo is not None:
    #             print(f'Главное фото - {url_main_photo.get("srcset")}')

    # Перевод списка в строку
    def __translate_list_to_string(self, _list):
        result = ''
        for item in _list:
            result += item + '\n'
        return result

    # Получение всей собранной инфомармации
    def get_info(self):
        name = self.__get_name()
        price = self.__get_price()

        specifications = self.__get_specifications()
        weight = specifications['вес']
        width = specifications['ширина']
        height = specifications['высота']
        model = specifications['модель']
        type_model = specifications['тип']
        brand = specifications['марка']
        manufacturer = specifications['изготовитель']
        volume = specifications['объем']

        all_photos = self.__get_all_photos_product()
        main_photo = all_photos['main-photo']
        additional_photos = all_photos['additional-photos']
        photo_articles = all_photos['photo-articles']

        description = self.__get_description()
        quantity_goods = self.__get_quantity_goods()

        return {
            'NAME': name,
            'PRICE': price,
            'WEIGHT': weight,
            'WIDTH': width,
            'HEIGHT': height,
            'MODEL': model,
            'TYPE_MODEL': type_model,
            'BRAND': brand,
            'MANUFACTURER': manufacturer,
            'VOLUME': volume,
            'MAIN_PHOTO': main_photo,
            'ADDITIONAL_PHOTOS': additional_photos,
            'PHOTO_ARTICLES': photo_articles,
            'DESCRIPTION': description,
            'QUANTITY_GOODS': quantity_goods,
            'URL': self.url
        }

        # self.__get_name()
        # self.__get_specifications()
        # self.__get_description()
        # self.__get_all_photos_product()
        # self.__get_quantity_goods()

