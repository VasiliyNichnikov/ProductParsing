"""
    Данный скрипт парсит объявление Leroy Merlin и получает ссылки.
"""
from scripts.GettingDriver import get_information_webdriver


class ParsingPage:
    def __init__(self, url, start_page, delay_after_error=0):
        self.url = url
        self.delay_after_error = delay_after_error
        self.number_now = start_page
        self.max = self.number_now + 1

    # Получение ссылок
    def get_urls(self):
        soup = get_information_webdriver(url=self.url + f'&page={self.number_now}', delay_after_error=self.delay_after_error)
        self.max = self.__get_max_page(soup=soup)
        block_urls = soup.find('div', {'class': ['cards-view-block', 'list', 'pedu908_plp', 'pr7cfcb_plp', 'largeCard']})
        if block_urls is not None:
            list_items = block_urls.find_all('div', {
                'class': ['c155f0re_plp', 'c1pkpd8l_plp', 'list']})
            return [f"https://perm.leroymerlin.ru{item.find('a').get('href')}" for item in list_items]
        else:
            return None

    # Удаление пробелов и enter
    @staticmethod
    def __removing_spaces_enter(value):
        return value.replace('\n', '').replace(' ', '')

    # Получение максимальной странице
    def __get_max_page(self, soup):
        list_max_page = [self.number_now]
        block_max_page = soup.find('div', {'class': 's1pmiv2e_plp'})
        # print(block_max_page)
        if block_max_page is not None:
            list_items = block_max_page.find_all('a', {'class': ['bex6mjh_plp', 'o1ojzgcq_plp', 'l7pdtbg_plp', 'r1yi03lb_plp', 'sj1tk7s_plp']})
            for item in list_items:
                number = item.find('span', {'class': 'cef202m_plp'})
                if number is not None and number.text is not None and number.text.isdigit():
                    list_max_page.append(int(number.text))
        return max(list_max_page)
