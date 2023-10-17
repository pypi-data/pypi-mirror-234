from pyquery import PyQuery as pq

from yandex_parser.exceptions import YandexParserError


class Elements:
    elements_class = '.serp-item.serp-item_card:not([data-fast-name]) .Organic'
    title_class = 'span.OrganicTitleContentSpan.organic__title'
    href_class = '.OrganicTitle-Link'
    description_classes = [('.Organic-ContentWrapper.organic__content-wrapper '
                            '.TextContainer.OrganicText.organic__text.text-container.Typo.Typo_text_m.Typo_line_m '
                            '.OrganicTextContentSpan'),
                           ('.Organic-ContentWrapper.organic__content-wrapper '
                            '.Organic-ByLink.Typo.Typo_text_m.Typo_line_m'),
                           ('.Organic-ContentWrapper.organic__content-wrapper '
                            '.OrganicForum-Item .OrganicForum-Text')]

    domen_class = '.Organic .Organic-Subtitle .Organic-Path b'


class YandexParser(Elements):
    default_snippet_fields = ('p', 'd', 'u', 't', 's')

    def __init__(self, html, snippet_fields=default_snippet_fields, exclude_market_yandex=True,
                 exclude_realty_yandex=True):
        self.html = html
        self.pq = pq(html) if html != '' else None
        self.snippet_fields = snippet_fields
        self.exclude_market_yandex = exclude_market_yandex
        self.exclude_realty_yandex = exclude_realty_yandex

    @property
    def snippets(self):
        return self.snippet_fields

    def _is_advertisement(self, doc_element):
        if href := doc_element(self.href_class).attr('href'):
            if 'https://yabs.yandex.ru' in href:
                return True

        return False

    def _is_yandex_market(self, doc_element):
        return doc_element(self.domen_class).text() == 'market.yandex.ru'

    def _is_yandex_realty(self, doc_element):
        return doc_element(self.domen_class).text() in ['realty.yandex.ru', 'realty.ya.ru']

    def is_yandex(self):
        if url := self.pq('meta[property="og:url"]').attr('content'):
            return 'yandex.ru' in url or 'ya.ru' in url
        return False

    def _get_description(self, doc_element):
        for description_class in self.description_classes:
            description = doc_element(description_class).text()
            if description:
                return description

    def _form_sn_data(self, doc_element, position):
        title = doc_element(self.title_class).text()
        href = doc_element(self.href_class).attr('href')
        description = self._get_description(doc_element)
        domain = doc_element(self.domen_class).text()

        if not title:
            raise YandexParserError('Title not found')

        if not href:
            raise YandexParserError('Href not found')

        if 'yabs.yandex.ru' in href:
            raise YandexParserError('Adv')

        if not domain:
            raise YandexParserError('Domen not found')

        sn_data = {snippet: None for snippet in self.default_snippet_fields}

        if 'p' in self.snippet_fields:
            sn_data['p'] = position
        if 'd' in self.snippet_fields:
            sn_data['d'] = domain.lower()
        if 'u' in self.snippet_fields:
            sn_data['u'] = href.lower()
        if 't' in self.snippet_fields:
            sn_data['t'] = title
        if 's' in self.snippet_fields:
            sn_data['s'] = description

        return sn_data

    def _handle_data(self):
        if not self.html:
            raise YandexParserError('Html is empty')

        if not self.is_yandex():
            raise YandexParserError('Html is not from yandex')

        elements = self.pq(self.elements_class)

        sn = []

        position = 0
        for element in elements:
            doc_element = pq(element)

            if self._is_advertisement(doc_element):
                continue

            if self.exclude_market_yandex and self._is_yandex_market(doc_element):
                continue

            if self.exclude_realty_yandex and self._is_yandex_realty(doc_element):
                continue

            position += 1
            if doc_element := self._form_sn_data(doc_element, position):
                sn.append(doc_element)

        return {'sn': sn, 'pc': None}

    def get_serp(self):
        try:
            return self._handle_data()
        except Exception as ex:
            raise YandexParserError(str(ex))
