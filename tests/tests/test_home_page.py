# coding=utf-8
import unittest
from tests.pages.home_page import HomePage
from tests.utils.data_utils import get_name_from_auto_suggestion
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
        home_page.search_for_what(u'ф')
        webdriver.implicitly_wait(3)
        addresses = webdriver.find_elements_by_xpath('//span[@data-bind="as-poi-address"]')
        ratings = webdriver.find_elements_by_xpath('//span[@data-bind="as-poi-rating"]')
        names = webdriver.find_elements_by_xpath('//p[@data-bind="as-poi-name"]')
        s_names = webdriver.find_elements_by_xpath('//p[@data-bind="as-poi-name"]/strong')
        categories = webdriver.find_elements_by_xpath('//li[@data-bind="as-category-name"]/a')
        aa = [x.text for x in addresses]
        nn = [get_name_from_auto_suggestion(x.text) for x in names]
        rr = [x.get_attribute('class') for x in ratings]
        ss = [x.text for x in s_names]
        cc = [x.text for x in categories]
        print '1'

if __name__ == "__main__":
    unittest.main()