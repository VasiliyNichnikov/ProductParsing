from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--log-level=3")
path_webdriver = '../files/chromium/chromedriver.exe'


def get_information(url, delay_after_error):
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
            sleep(5 * 60)
