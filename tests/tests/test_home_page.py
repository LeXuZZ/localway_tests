# coding=utf-8
import unittest
from tests.pages.home_page import HomePage
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
        self.assertTrue(home_page.search_what_input().is_displayed(), 'search what input is not displayed')
        self.assertTrue(home_page.search_where_input().is_displayed(), 'search where input is not displayed')
        self.assertTrue(home_page.search_button().is_displayed(), 'search button input is not displayed')

    def test_max_input_50_symbols_in_what_search_field(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what("Lorem ipsum dolor sit amet, consectetur adipisicinUNNECESSARYSYMBOLS")
        self.assertEqual(50, len(home_page.search_what_input().get_attribute('value')),
                         'invalid maximum number of characters in what search field')

    def test_max_input_50_symbols_in_where_search_field(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_where("Lorem ipsum dolor sit amet, consectetur adipisicinUNNECESSARYSYMBOLS")
        self.assertEqual(50, len(home_page.search_where_input().get_attribute('value')),
                         'invalid maximum number of characters in where search field')

    def test_search_button_is_disabled(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        self.assertFalse(home_page.search_button().is_enabled(), 'search button is not disabled')

    def test_search_button_is_enabled_when_what_search_input_not_empty(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what('some text')
        self.assertTrue(home_page.search_button().is_enabled(), 'search button is disabled')

    def test_search_button_is_enabled_when_where_search_input_not_empty(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_where('some text')
        self.assertTrue(home_page.search_button().is_enabled(), 'search button is disabled')

    def test_auto_suggestion(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u'рест')
        webdriver.implicitly_wait(5)
        suggestion_from_page = home_page.get_autosuggestion()
        stub_data = create_stub_data_for_autosuggestion()
        self.assertEqual(suggestion_from_page, stub_data)
        print '1'

if __name__ == "__main__":
    unittest.main()