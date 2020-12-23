"""
    Данный скрипт парсит страницу Ozon и получает все ссылки.
"""

from scripts.GettingDriver import init_driver, get_driver
from bs4 import BeautifulSoup


url = 'https://www.ozon.ru/category/smartfony-15502/?from_global=true&text=телефон'


init_driver()
driver = get_driver()
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'lxml')

block_goods = soup.find('div', {'class': 'ao4'})
if block_goods is not None:
    goods = block_goods.find_all('div', {'class': ['a0c6', 'a0c9', 'a0c8']})
    if goods is not None:
        for product in goods:
            print('https://www.ozon.ru' + product.find('a', {'class': ['a0v2', 'tile-hover-target']}).get('href'))
driver.close()








