""""
    Парсинг страниц магазина лента.
    Страница - https://lenta.com/search/?page=1&searchText=%D0%B3%D1%80%D0%B5%D1%87%D0%BA%D0%B0
"""
from scripts.getting_driver import get_information_requests, get_information_webdriver


class ParsingPageLenta:
    def __init__(self, url, start_page, delay_after_error=0):
        self.url = url
        self.delay_after_error = delay_after_error
        self.page = start_page
        self.max_page = self.page + 1

    # Получение ссылок
    def get_urls(self):
        soup = get_information_webdriver(url=self.url + f'&page={self.page}', delay_after_error=self.delay_after_error)
        block_main = soup.find('div', {'class': 'skus-search-results__main'})
        block_products = block_main.find('div', {'class': 'catalog-grid-container__grid'})

        if block_products is not None:
            products = block_products.find_all('div', {'class': 'sku-card-small-container'})
            print(products)
            # for product in products:
            #     print(product.find('a', {'class': 'sku-card-small sku-card-small--ecom'}))

        # soup = get_information_requests(url=self.url + f'&page={self.page}', delay_after_error=self.delay_after_error)
        # self.max_page = self.__get_max_page(soup=soup)
        # block_urls = soup.find('div',
        #                        {'class': ['cards-view-block', 'list', 'pedu908_plp', 'filtered-products-wrapper']})
        # if block_urls is not None:
        #     list_items = block_urls.find_all('div', {
        #         'class': ['c155f0re_plp', 'c1pkpd8l_plp', 'list']})
        #     if len(list_items) == 0:
        #         list_items = block_urls.find_all('uc-plp-item-new')
        #         return [f"https://perm.leroymerlin.ru{item.get('href')}" for item in list_items]
        #     return [f"https://perm.leroymerlin.ru{item.find('a').get('href')}" for item in list_items]

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


url = "https://lenta.com/search/?searchText=%D0%B3%D1%80%D0%B5%D1%87%D0%BA%D0%B0"
if __name__ == '__main__':
    parsing_page_lenta = ParsingPageLenta(url, 1)
    parsing_page_lenta.get_urls()
