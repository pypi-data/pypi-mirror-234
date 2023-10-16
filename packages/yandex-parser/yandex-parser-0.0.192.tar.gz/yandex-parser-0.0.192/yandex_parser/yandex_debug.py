from pprint import pprint

from yandex_parser import YandexParser
from yandex_parser.tests.test_yandex import BaseYandexParserTest

parser = YandexParser(BaseYandexParserTest().get_data('case15--ignore-advertisement3-parser-data.html'))
pprint(parser.get_serp())
