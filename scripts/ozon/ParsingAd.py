"""
    Данный скрипт парсит объявление Ozon и получает цену, описание товара и сохранение фото.
"""

from scripts.GettingDriver import init_driver, get_driver
from bs4 import BeautifulSoup


url = 'https://www.ozon.ru/product/smartfon-xiaomi-redmi-note-9-4-128gb-seryy-177823201/?asb=X3RTeILEfWwDjqE1bXHPfo6jM3mNi2S2wpBCEF9UIT4%253D'


init_driver()
driver = get_driver()
driver.get(url)
soup = BeautifulSoup(driver.page_source, 'lxml')

# Получение названия товара
block_description = soup.find('div', {'data-widget': 'webProductHeading'})
if block_description is not None:
    description = soup.find('h1', {'class': 'b3a8'}).text
    print(description)

# Получение цены
price = soup.find('span', {'class': 'c8q7'}).text
print(price)

# Получение цены до скидки
price_before_discount = soup.find('span', {'class': 'c8r'}).text
print(price_before_discount)

# Получение цены с ozon premium
# price_ozon_premium = soup.find()

# Получение ozon id
ozon_id = soup.find('span', {'class': ['b2d7', 'b2d9']}).text
print(ozon_id)




driver.close()








