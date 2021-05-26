from bs4 import BeautifulSoup, PageElement, ResultSet
from scripts.errors import TagInformationNotFound


def check_result(result, name_tag):
    if result is not None:
        return result
    else:
        raise TagInformationNotFound(f"Tag information({name_tag}) not found")


class HandlerSoup:
    def __init__(self, soup: BeautifulSoup):
        self.soup = soup

    def find(self, name=None, attrs={}, recursive=True, text=None,
             **kwargs) -> PageElement:
        result = self.soup.find(name, attrs, recursive, text, **kwargs)

        try:
            return check_result(result, name)
        except TagInformationNotFound as e:
            print("Error - %s" % e)
        return PageElement()

    def find_all(self, name=None, attrs={}, recursive=True, text=None,
                 limit=None, **kwargs) -> ResultSet:
        result = self.soup.find_all(name, attrs, recursive, text, limit, **kwargs)
        try:
            return check_result(result, name)
        except TagInformationNotFound as e:
            print("Error - %s" % e)
        return ResultSet(object)
