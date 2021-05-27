from scripts.lenta.parse_ad import ParseAd
import unittest


class ParseAdBuckwheatTest(unittest.TestCase):
    __url = "https://lenta.com/product/grechka-mistral-fermerskaya-rossiya-900g-479051/"

    def setUp(self) -> None:
        self.parsing_ad = ParseAd(self.__url, "", 0)

    def test_get_article_number(self):
        answer_func = self.parsing_ad._ParseAd__get_article_number()
        right_result = 479051
        self.assertEqual(answer_func, right_result)

    def test_get_name(self):
        answer_func = self.parsing_ad._ParseAd__get_name()
        right_result = "Гречка МИСТРАЛЬ Фермерская, Россия, 900 г"
        self.assertEqual(answer_func, right_result)

    def test_get_default_lenta_card_prices(self):
        answer_func = self.parsing_ad._ParseAd__get_default_lenta_card_prices()
        right_result = {'default': '157.19', 'lenta_card': '99.89'}
        self.assertEqual(answer_func, right_result)


class ParseAdNoneTest(unittest.TestCase):
    __url = "https://lenta.com/product/none/"

    def setUp(self) -> None:
        self.parsing_ad = ParseAd(self.__url, "", 0)

    def test_get_article_number(self):
        answer_func = self.parsing_ad._ParseAd__get_article_number()
        right_result = 1
        self.assertNotEqual(answer_func, right_result)

    def test_get_name(self):
        answer_func = self.parsing_ad._ParseAd__get_name()
        right_result = "None"
        self.assertNotEqual(answer_func, right_result)

    def test_get_default_lenta_card_prices(self):
        answer_func = self.parsing_ad._ParseAd__get_default_lenta_card_prices()
        right_result = {'default': '', 'lenta_card': ''}
        self.assertNotEqual(answer_func, right_result)


if __name__ == '__main__':
    unittest.main()
