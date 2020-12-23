"""
    Данный скрипт парсит объявление Leroy Merlin и получает ссылки.
"""
from scripts.GettingDriver import get_information


class ParsingPage:
    def __init__(self, url, start_page):
        self.url = url
        self.page = start_page
        self.max_page = self.page + 1

    # Получение ссылок
    def get_urls(self):
        soup = get_information(url=self.url + f'&page={self.page}')
        self.max_page = self.__get_max_page(soup=soup)
        block_urls = soup.find('div', {'class': ['cards-view-block', 'list']})
        if block_urls is not None:
            _block_urls = block_urls.find('div', {'data-element-id': 'plp-card-list', 'class': 'plp-card-list'})
            if _block_urls is not None:
                list_items = _block_urls.find_all('product-card')
                return [f"https://leroymerlin.ru{item.find('uc-plp-item-new').get('href')}" for item in list_items]

    # Удаление пробелов и enter
    def __removing_spaces_enter(self, value):
        return value.replace('\n', '').replace(' ', '')

    # Получение максимальной странице
    def __get_max_page(self, soup):
        list_max_page = [self.page]
        block_max_page = soup.find('div', {'class': 'items-wrapper'})
        if block_max_page is not None:
            list_items = block_max_page.find_all('div', {'class': 'item-wrapper'})
            for item in list_items:
                _a = item.find('a')
                if _a is not None:
                    list_max_page.append(int(self.__removing_spaces_enter(_a.text)))
        return max(list_max_page)


