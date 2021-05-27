from bs4 import BeautifulSoup, PageElement, ResultSet
from scripts.errors import TagInformationNotFound, TextTagNotFound


def check_result(result, name_tag):
    if result is not None:
        return True
    else:
        raise TagInformationNotFound(f"Tag information({name_tag}) not found")


def check_text(result, name_tag):
    if result is not None:
        return True
    else:
        raise TextTagNotFound(f"Text in tag ({name_tag}) not found")


class HandlerSoup:
    def text(self, soup: BeautifulSoup):
        text = check_text(soup.text, soup.name)
        # try:
        #     text = check_text(soup.text, soup.name)
        # except TextTagNotFound as e:
        #     print(f"Error - %s" % e)
        return text

    def find(self, soup: BeautifulSoup, name=None, attrs={}, recursive=True, text=None,
             **kwargs) -> PageElement:
        result = soup.find(name, attrs, recursive, text, **kwargs)
        check_result(result, name)
        return result
        # result = None
        # try:
        #     result = soup.find(name, attrs, recursive, text, **kwargs)
        #     check_result(result, name)
        # except TagInformationNotFound as e:
        #     print("Error - %s" % e)
        # except AttributeError as e:
        #     print("Error - %s" % e)
        # return result

    def find_all(self, soup: BeautifulSoup, name=None, attrs={}, recursive=True, text=None,
                 limit=None, **kwargs):
        result = None
        try:
            result = soup.find_all(name, attrs, recursive, text, limit, **kwargs)
            check_result(result, name)
        except TagInformationNotFound as e:
            print("Error - %s" % e)
        except AttributeError as e:
            print("Error - %s" % e)
        return result


class HandlerSoup2:
    def __init__(self, soup: [BeautifulSoup, PageElement, ResultSet]):
        self.__soup = soup

    @property
    def soup(self) -> [BeautifulSoup, PageElement, ResultSet]:
        return self.__soup

    @soup.setter
    def soup(self, value: [BeautifulSoup, PageElement, ResultSet]):
        self.__soup = value

    @property
    def text(self) -> str:
        try:
            result = self.__soup.text
            check_text(result, self.__soup.name)
            return result
        except TextTagNotFound as e:
            print("Error - %s" % e)
        except AttributeError as e:
            print("Error - %s" % e)
        return str()

    def find(self, name=None, attrs={}, recursive=True, text=None,
             **kwargs) -> PageElement:
        try:
            result = self.__soup.find(name, attrs, recursive, text, **kwargs)
            check_result(result, name)
            return result
        except TagInformationNotFound as e:
            print("Error - %s" % e)
        except AttributeError as e:
            print("Error - %s" % e)
        return PageElement()

    def find_all(self, name=None, attrs={}, recursive=True, text=None,
                 limit=None, **kwargs):
        result = None
        try:
            result = self.__soup.find_all(name, attrs, recursive, text, limit, **kwargs)
            check_result(result, name)
        except TagInformationNotFound as e:
            print("Error - %s" % e)
        except AttributeError as e:
            print("Error - %s" % e)
        # return HandlerSoup2(result)

    # @property
    # def text(self):
    #     text = ""
    #     try:
    #         text = self.soup.text
    #     except AttributeError as e:
    #         print("Error - %s" % e)
    #     return text
