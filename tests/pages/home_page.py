import re
from tests.pages.block_objects import HeaderBlock, FooterBlock, AutoSuggestion

__author__ = 'lxz'

from wtframework.wtf.web.page import PageObject, InvalidPageError


class HomePage(PageObject, HeaderBlock, FooterBlock, AutoSuggestion):


    ### Page Elements Section ###
    search_what_input = lambda self: self.webdriver.find_element_by_id(
        "input-what")
    search_where_input = lambda self: self.webdriver.find_element_by_id(
        "input-where")
    search_button = lambda self: self.webdriver.find_element_by_xpath(
        "/html/body/section/section/section/section/form/button")
    ### End Page Elements Section ###

    def _validate_page(self, webdriver):

        if not re.search('Localway', webdriver.title):
            raise InvalidPageError("This page did not pass HomePage page validation.")

    def search_for_what(self, search_string):
        self.search_what_input().clear()
        self.search_what_input().send_keys(search_string)

    def search_for_where(self, search_string):
        self.search_where_input().clear()
        self.search_where_input().send_keys(search_string)

    def click_search_button(self):
        # ActionChains(self.webdriver).move_to_element_with_offset(self.search_button(), 5, -5).click().perform()
        self.search_button().click()
