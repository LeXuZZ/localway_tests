# coding=utf-8
import unittest
from selenium.webdriver.common.keys import Keys
from tests.pages import ResultsList
from tests.pages.home_page import HomePage
from tests.pages.poi_page import POIPage
from wtframework.wtf.utils.json_utils import YandexAPI, SearchAPI, POI_JSON
from wtframework.wtf.utils.mongo_utils import MongoDB
from wtframework.wtf.web.page import PageFactory
from wtframework.wtf.config import ConfigReader
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER

__author__ = 'lxz'


class HomePageTest(WTFBaseTest):
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

    def test_search_only_with_what(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.click_search_button()
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsList, webdriver)
        self.assertGreater(len(results_list_page.poi_list_articles()), 1)

    def test_search_only_with_what_by_enter(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.search_what_input().send_keys(Keys.RETURN)
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsList, webdriver)
        self.assertGreater(len(results_list_page.poi_list_articles()), 1)

    def test_search_only_with_where_by_enter(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_where(u"Москва")
        home_page.search_where_input().send_keys(Keys.RETURN)
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsList, webdriver)
        self.assertGreater(len(results_list_page.poi_list_articles()), 1)

    def test_search_only_with_what_but_with_focus_on_when_by_enter(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.search_where_input().send_keys(Keys.RETURN)
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsList, webdriver)
        self.assertGreater(len(results_list_page.poi_list_articles()), 1)

    def test_search_only_with_where_when_yandex_found_greater_than_0(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        query = u"Москва"
        found_count = YandexAPI().get_found_count(query)
        self.assertGreater(found_count, 0)
        home_page.search_for_where(query)
        home_page.click_search_button()
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsList, webdriver)
        self.assertGreater(len(results_list_page.poi_list_articles()), 1, 'POI list is empty')

    def test_search_only_with_where_when_found_equals_0(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        query = 'UNACCEPTABLE'
        found_count = YandexAPI().get_found_count(query)
        self.assertEqual('0', found_count)
        home_page.search_for_where(query)
        home_page.click_search_button()
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsList, webdriver)
        self.assertEqual(u'Ничего не найдено', results_list_page.poi_place_holder().text,
                         'POI list is not empty. Message \'Nothing found\' is not displayed')

    def test_pagination_existence_true_scenario(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        query = u"Бар"
        self.assertGreater(SearchAPI().get_total_count(query), SearchAPI().get_count_on_page(query),
                           'Need to change the What query')
        home_page.search_for_what(query)
        home_page.click_search_button()
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsList, webdriver)
        self.assertTrue(results_list_page.pagination_panel().is_displayed())

    def test_pagination_existence_false_scenario(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        query = u"Дельфин"
        self.assertLess(SearchAPI().get_total_count(query), SearchAPI().get_count_on_page(query),
                        'Need to change the What query')
        home_page.search_for_what(query)
        home_page.click_search_button()
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsList, webdriver)
        self.assertFalse(results_list_page.pagination_panel().is_displayed())

    def test_yandex_map_existence_true_scenario(self):
        poi_id_with_yandex_map = '162239af0000000000000000'
        webdriver = self.set_up()
        webdriver.get(ConfigReader('site_credentials').get("default_url") + '#poi/' + poi_id_with_yandex_map)
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        self.assertIsNotNone(POI_JSON(poi_id_with_yandex_map).lat)
        self.assertIsNotNone(POI_JSON(poi_id_with_yandex_map).lon)
        self.assertTrue(poi_page.yandex_map().is_displayed())

    def test_yandex_map_existence_false_scenario(self):
        poi_id_without_yandex_map = '161708af0000000000000000'
        webdriver = self.set_up()
        webdriver.get(ConfigReader('site_credentials').get("default_url") + '#poi/' + poi_id_without_yandex_map)
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        self.assertIsNone(POI_JSON(poi_id_without_yandex_map).lat)
        self.assertIsNone(POI_JSON(poi_id_without_yandex_map).lon)
        self.assertFalse(poi_page.yandex_map().is_displayed())

    def test_cuisine_is_shown(self):
        random_poi_id_with_cuisines = MongoDB().get_random_poi_id_with_cuisines()
        webdriver = self.set_up()
        webdriver.get(
            ConfigReader('site_credentials').get("default_url") + '#poi/' + str(random_poi_id_with_cuisines))
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        self.assertGreater(len(poi_page.cuisines()), 0, "block cuisines does not exist")

    def test_cuisine_is_not_shown(self):
        random_poi_id_without_cuisines = MongoDB().get_random_poi_id_without_cuisines()
        webdriver = self.set_up()
        webdriver.get(
            ConfigReader('site_credentials').get("default_url") + '#poi/' + str(random_poi_id_without_cuisines))
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        self.assertEqual(len(poi_page.cuisines()), 0, "block cuisines does exist")

        # def test_hotel_stars_and_check_io_is_shown(self):
        #     poi_with_hotel_stars_and_check_io = MongoDB().get_poi_with_hotel_stars_and_check_io()
        #     webdriver = self.set_up()
        #     webdriver.get(webdriver.get(ConfigReader('site_credentials').get("default_url")) + '#poi/' + str(poi_with_hotel_stars_and_check_io))
        #     webdriver.implicitly_wait(20)
        #     poi_page = PageFactory.create_page(POIPage, webdriver)
        #     print '1'


if __name__ == "__main__":
    unittest.main()