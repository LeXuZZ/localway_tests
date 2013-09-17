import re
from wtframework.wtf.web.webelement import WebElementSelector, WebElementUtils
from tests.pages.block_objects import HeaderBlock, FooterBlock, AutoSuggestion, SearchBlock

__author__ = 'lxz'

from wtframework.wtf.web.page import PageObject, InvalidPageError


class HomePage(PageObject, HeaderBlock, FooterBlock, AutoSuggestion, SearchBlock):


    ### Page Elements Section ###
    ### End Page Elements Section ###

    def _validate_page(self, webdriver):

        if not re.search('Localway', webdriver.title):
            raise InvalidPageError("This page did not pass HomePage page validation.")

    def search_for_what(self, search_string):
        self.search_what_input().clear()
        self.webdriver.implicitly_wait(3)
        self.search_what_input().send_keys(search_string)

    def search_for_where(self, search_string):
        self.search_where_input().clear()
        self.webdriver.implicitly_wait(3)
        self.search_where_input().send_keys(search_string)

    def click_search_button(self):
        # ActionChains(self.webdriver).move_to_element_with_offset(self.search_button(), 5, -5).click().perform()
        WebElementUtils.check_is_displayed(self.webdriver, self.search_button())
        self.search_button().click()
