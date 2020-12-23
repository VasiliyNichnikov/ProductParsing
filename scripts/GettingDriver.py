from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from selenium.common.exceptions import WebDriverException


options = webdriver.ChromeOptions()
options.add_argument('--headless')
path_webdriver = '../files/chromium/chromedriver'


def get_information(url):
    for i in range(10):
        try:
            with webdriver.Chrome(executable_path=path_webdriver, options=options) as driver:
                driver.get(url)
                return BeautifulSoup(driver.page_source, 'lxml')
        except WebDriverException as e:
            print('Ошибка - %s' % e)
            sleep(5 * 60)

