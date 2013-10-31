# coding=utf-8
import unittest
from tests.pages.home_page import HomePage
from tests.utils.checkers import *
from tests.utils.data_utils import get_name_from_auto_suggestion, create_stub_data_for_autosuggestion
from wtframework.wtf.web.page import PageFactory
from wtframework.wtf.config import ConfigReader
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER

__author__ = 'lxz'


class HomePageTest(WTFBaseTest):

    maxDiff = None

    def set_up(self):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(ConfigReader('site_credentials').get("default_url"))
        return webdriver

    def test_elements_existence(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        verify_if_displayed(home_page.search_what_input)
        verify_if_displayed(home_page.search_where_input)
        verify_if_displayed(home_page.search_button)

    #ADDED
    def test_max_input_50_symbols_in_what_search_field(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        verify_max_length_of_field(home_page.search_what_input, 50)

    #ADDED
    def test_max_input_50_symbols_in_where_search_field(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        verify_max_length_of_field(home_page.search_where_input, 50)

    #ADDED
    def test_search_button_is_disabled(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        verify_if_disabled(home_page.search_button)

    #ADDED
    def test_search_button_is_enabled_when_what_search_input_not_empty(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what('some text')
        verify_if_enabled(home_page.search_button)

    #ADDED
    def test_search_button_is_enabled_when_where_search_input_not_empty(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_where('some text')
        verify_if_enabled(home_page.search_button)

    #ADDED
    def test_auto_suggestion(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u'рест')
        webdriver.implicitly_wait(5)
        suggestion_from_page = home_page.get_autosuggestion()
        stub_data = create_stub_data_for_autosuggestion()
        assert_that(suggestion_from_page, equal_to(stub_data))

if __name__ == "__main__":
    unittest.main()