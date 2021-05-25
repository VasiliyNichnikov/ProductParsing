from bs4 import BeautifulSoup
from scripts.errors import TagInformationNotFound


def check_result(result, name_tag):
    if result is not None:
        return result
    else:
        raise TagInformationNotFound(f"Tag information({name_tag}) not found")


class HandlerSoup:
    def find(self, soup: BeautifulSoup, name=None, attrs={}, recursive=True, text=None,
             **kwargs) -> BeautifulSoup:
        result = soup.find(name, attrs, recursive, text, **kwargs)
        return check_result(result, name)

    def find_all(self, soup: BeautifulSoup, name=None, attrs={}, recursive=True, text=None,
                 limit=None, **kwargs) -> BeautifulSoup:
        result = soup.find_all(name, attrs, recursive, text, limit, **kwargs)
        return check_result(result, name)
