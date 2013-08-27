# coding=utf-8
import unittest

from selenium.webdriver.common.keys import Keys

from tests.pages import HomePage, ResultsListPage
from tests.pages.none_results_page import NoneResultsList
from tests.utils.json_utils import SearchAPI, YandexAPI
from wtframework.wtf.web.page import PageFactory
from wtframework.wtf.config import ConfigReader
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER


__author__ = 'lxz'


class ResultsPageTest(WTFBaseTest):

    maxDiff = None

    def set_up(self):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(ConfigReader('site_credentials').get("default_url"))
        return webdriver

    def test_search_only_with_where_when_found_equals_0(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        query = 'UNACCEPTABLE'
        found_count = YandexAPI().get_found_count(query)
        self.assertEqual('0', found_count)
        home_page.search_for_where(query)
        home_page.click_search_button()
        webdriver.implicitly_wait(20)
        none_results_page = PageFactory.create_page(NoneResultsList, webdriver)
        none_results_page.check_text_presence()

    def test_pagination_existence_true_scenario(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        query = u"Бар"
        self.assertGreater(SearchAPI().get_total_count(query), SearchAPI().get_count_on_page(query),
                           'Need to change the What query')
        home_page.search_for_what(query)
        home_page.click_search_button()
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertTrue(results_list_page.pagination_panel().is_displayed())

    def test_pagination_existence_false_scenario(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        query = u"Дельфин"
        self.assertLessEqual(SearchAPI().get_total_count(query), SearchAPI().get_count_on_page(query),
                             'Need to change the What query')
        home_page.search_for_what(query)
        home_page.click_search_button()
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertFalse(results_list_page.pagination_panel().is_displayed())

    def test_search_only_with_what(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.click_search_button()
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertGreater(len(results_list_page.articles()), 1)

    def test_search_only_with_what_by_enter(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.search_what_input().send_keys(Keys.RETURN)
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertGreater(len(results_list_page.articles()), 1)

    def test_search_only_with_where_by_enter(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_where(u"Москва")
        home_page.search_where_input().send_keys(Keys.RETURN)
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertGreater(len(results_list_page.articles()), 1)

    def test_search_only_with_what_but_with_focus_on_when_by_enter(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.search_where_input().send_keys(Keys.RETURN)
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertGreater(len(results_list_page.articles()), 1)

    def test_search_only_with_where_when_yandex_found_greater_than_0(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        query = u"Москва"
        found_count = YandexAPI().get_found_count(query)
        self.assertGreater(found_count, 0)
        home_page.search_for_where(query)
        home_page.click_search_button()
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertGreater(len(results_list_page.articles()), 1, 'POI list is empty')

if __name__ == "__main__":
    unittest.main()