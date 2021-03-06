from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests
from requests import HTTPError
from .errors import ErrorInformationPageNotFound
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
options.add_argument("--log-level=3")
path_webdriver = '../../files/chromium/chromedriver'


def get_information_webdriver(url, delay_after_error):
    for i in range(10):
        try:
            with webdriver.Chrome(executable_path=path_webdriver, options=options) as driver:
                driver.get(url)
                return BeautifulSoup(driver.page_source, 'lxml')

        except TimeoutException as e:
            print('Ошибка - %s' % e)
            sleep(delay_after_error)

        except NoSuchElementException as e:
            print('Ошибка - %s' % e)
            sleep(delay_after_error)

        except WebDriverException as e:
            print('Ошибка - %s' % e)
            sleep(delay_after_error)
    raise ErrorInformationPageNotFound('Информация не найдена')


def get_information_requests(url, delay_after_error):
    for i in range(10):
        try:
            session = requests.Session()
            response = session.get(url)

            # with open("test_html.html", "w", encoding="utf-8") as file_write:
            #     file_write.write(response.text)
            print("BS4 - ", BeautifulSoup(response.text, 'lxml'))
            return BeautifulSoup(response.text, 'lxml')

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
            sleep(delay_after_error)

        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
            sleep(delay_after_error)
    raise ErrorInformationPageNotFound('Информация не найдена')
