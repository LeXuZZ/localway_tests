import re

__author__ = 'lxz'

from wtframework.wtf.web.page import PageObject, InvalidPageError


class HomePage(PageObject):
    '''
    HomePage
    WTFramework PageObject representing a page like:
    http://172.31.237.12/
    '''


    ### Page Elements Section ###
    search_what_input = lambda self: self.webdriver.find_element_by_id(
        "input-what")
    search_where_input = lambda self: self.webdriver.find_element_by_id(
        "input-where")
    search_button = lambda self: self.webdriver.find_element_by_xpath(
        "/html/body/section/section/section/section[1]/form/button")
    ### End Page Elements Section ###


    def _validate_page(self, webdriver):
        '''
        Validates we are on the correct page.
        '''

        if not re.search("Localway", webdriver.title):
            raise InvalidPageError("This page did not pass ResultsListPage page validation.")

    def search_for_what(self, search_string):
        # We can call a mapped element by calling it's lambda function.
        self.search_what_input().clear()
        self.search_what_input().send_keys(search_string)

    def search_for_where(self, search_string):
        # We can call a mapped element by calling it's lambda function.
        self.search_where_input().clear()
        self.search_where_input().send_keys(search_string)

    def click_search_button(self):
        self.search_button().click()
