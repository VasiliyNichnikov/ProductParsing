from bs4 import BeautifulSoup
from scripts.Errors import TagInformationNotFound


def check_result(result, name_tag):
    if result is not None:
        return result
    else:
        raise TagInformationNotFound(f"Tag information({name_tag}) not found")


class HandlerSoup:
    def __init__(self, soup) -> None:
        self.soup = soup

    def find(self, name=None, attrs={}, recursive=True, text=None,
             **kwargs) -> BeautifulSoup:
        result = self.soup.find(name, attrs, recursive, text, **kwargs)
        return check_result(result, name)

    def find_all(self, name=None, attrs={}, recursive=True, text=None,
                 limit=None, **kwargs) -> BeautifulSoup:
        result = self.soup.find_all(name, attrs, recursive, text, limit, **kwargs)
        return check_result(result, name)
