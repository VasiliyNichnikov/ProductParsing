from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests
from requests import HTTPError
from Errors import ErrorInformationPageNotFound
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--log-level=3")
path_webdriver = '../files/chromium/chromedriver.exe'


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
            response = requests.get(url)
            # если ответ успешен, исключения задействованы не будут
            response.raise_for_status()
            return BeautifulSoup(response.text, 'lxml')

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
            sleep(delay_after_error)

        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
            sleep(delay_after_error)
    raise ErrorInformationPageNotFound('Информация не найдена')