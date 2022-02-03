"""
    Данный скрипт парсит объявление Leroy Merlin и получает ссылки.
"""
from scripts.GettingDriver import get_information_webdriver


class ParsingPage:
    def __init__(self, url, start_page, delay_after_error=0):
        self.url = url
        self.delay_after_error = delay_after_error
        self.page = start_page
        self.max_page = self.page + 1

    # Получение ссылок
    def get_urls(self):
        soup = get_information_webdriver(url=self.url + f'&page={self.page}', delay_after_error=self.delay_after_error)
        self.max_page = self.__get_max_page(soup=soup)
        # print(self.max_page)
        block_urls = soup.find('div', {'class': ['cards-view-block', 'list', 'pedu908_plp', 'pr7cfcb_plp', 'largeCard']})
        # print(block_urls)
        if block_urls is not None:
            list_items = block_urls.find_all('div', {
                'class': ['c155f0re_plp', 'c1pkpd8l_plp', 'list']})
            # print(list_items)
            return [f"https://perm.leroymerlin.ru{item.find('a').get('href')}" for item in list_items]
        else:
            pass # FIXME ошибка

    # Удаление пробелов и enter
    def __removing_spaces_enter(self, value):
        return value.replace('\n', '').replace(' ', '')

    # Получение максимальной странице
    def __get_max_page(self, soup):
        list_max_page = [self.page]
        block_max_page = soup.find('div', {'class': 's1pmiv2e_plp'})
        # print(block_max_page)
        if block_max_page is not None:
            list_items = block_max_page.find_all('a', {'class': ['bex6mjh_plp', 'o1ojzgcq_plp', 'l7pdtbg_plp', 'r1yi03lb_plp', 'sj1tk7s_plp']})
            print(list_items)
            for item in list_items:
                number = item.find('span', {'class': 'cef202m_plp'})
                print(number)
                if number is not None and number.text is not None and number.text.isdigit():
                    list_max_page.append(int(number.text))
        return max(list_max_page)
