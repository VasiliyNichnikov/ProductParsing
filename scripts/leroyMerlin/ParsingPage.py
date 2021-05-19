"""
    Данный скрипт парсит объявление Leroy Merlin и получает ссылки.
"""
from scripts.GettingDriver import get_information_requests


class ParsingPage:
    def __init__(self, url, start_page, delay_after_error=0):
        self.url = url
        self.delay_after_error = delay_after_error
        self.page = start_page
        self.max_page = self.page + 1

    # Получение ссылок
    def get_urls(self):
        soup = get_information_requests(url=self.url + f'&page={self.page}', delay_after_error=self.delay_after_error)
        self.max_page = self.__get_max_page(soup=soup)
        block_urls = soup.find('div', {'class': ['cards-view-block', 'list', 'pedu908_plp', 'filtered-products-wrapper']})
        if block_urls is not None:
            list_items = block_urls.find_all('div', {
                'class': ['c155f0re_plp', 'c1pkpd8l_plp', 'list']})
            if len(list_items) == 0:
                list_items = block_urls.find_all('uc-plp-item-new')
                return [f"https://perm.leroymerlin.ru{item.get('href')}" for item in list_items]
            return [f"https://perm.leroymerlin.ru{item.find('a').get('href')}" for item in list_items]

    # Удаление пробелов и enter
    def __removing_spaces_enter(self, value):
        return value.replace('\n', '').replace(' ', '')

    # Получение максимальной странице
    def __get_max_page(self, soup):
        list_max_page = [self.page]
        block_max_page = soup.find('div', {'class': 's1pmiv2e_plp'})
        if block_max_page is not None:
            list_items = block_max_page.find_all('a', {
                'class': ['bex6mjh_plp', 'o1ojzgcq_plp', 'l7pdtbg_plp', 'r1yi03lb_plp', 'sj1tk7s_plp', 'irhr125_plp']})
            for item in list_items:
                _a = item.get('data-qa-pagination-item')
                if _a is not None and _a != 'right' and _a != 'left':
                    _a.replace(' ', '')
                    list_max_page.append(int(_a))
        return max(list_max_page)
