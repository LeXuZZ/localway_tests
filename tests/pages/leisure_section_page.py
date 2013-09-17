import re
from tests.pages.block_objects import HeaderBlock, FooterBlock, SearchBlock
from wtframework.wtf.web.page import PageObject, InvalidPageError

__author__ = 'lxz'


class LeisureSectionPage(PageObject, HeaderBlock, FooterBlock, SearchBlock):

    def _validate_page(self, webdriver):

        if not re.search('Localway', webdriver.title):
            raise InvalidPageError("This page did not pass HomePage page validation.")