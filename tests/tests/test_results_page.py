# coding=utf-8
from random import choice, randrange
import unittest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
import time
from tests.pages.block_objects import LocateMe
from tests.pages.poi_page import POIPage
from tests.static.constants import POI_KEYS
from tests.utils.data_utils import round_distance
from wtframework.wtf.web.webelement import WebElementUtils

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

    def set_up_with_suffix(self, suffix):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(ConfigReader('site_credentials').get("default_url") + suffix)
        return webdriver

    #ADDED
    def test_search_only_with_where_when_found_equals_0(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        query = 'UNACCEPTABLE'
        found_count = YandexAPI.get_found_count(query)
        self.assertEqual('0', found_count)
        home_page.search_for_where(query)
        home_page.click_search_button()
        webdriver.implicitly_wait(5)
        none_results_page = PageFactory.create_page(NoneResultsList, webdriver)
        none_results_page.check_text_presence()

    #ADDDED
    def test_pagination_existence_true_scenario(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        query = u"Бар"
        self.assertGreater(SearchAPI.get_total_count(query), SearchAPI.get_count_on_page(query),
                           'Need to change the What query')
        home_page.search_for_what(query)
        home_page.click_search_button()
        webdriver.implicitly_wait(5)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertTrue(results_list_page.pagination_panel().is_displayed())

    #ADDED
    def test_pagination_existence_false_scenario(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        query = u"Дельфин"
        self.assertLessEqual(SearchAPI.get_total_count(query), SearchAPI.get_count_on_page(query),
                             'Need to change the What query')
        home_page.search_for_what(query)
        home_page.click_search_button()
        webdriver.implicitly_wait(5)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertFalse(results_list_page.pagination_panel().is_displayed())

    #ADDED
    def test_search_only_with_what(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.click_search_button()
        webdriver.implicitly_wait(5)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertGreater(len(results_list_page.articles()), 1)

    #ADDED
    def test_search_only_with_what_by_enter(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.search_what_input().send_keys(Keys.RETURN)
        webdriver.implicitly_wait(5)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertGreater(len(results_list_page.articles()), 1)

    #ADDED
    def test_search_only_with_where_by_enter(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_where(u"Москва")
        home_page.search_where_input().send_keys(Keys.RETURN)
        webdriver.implicitly_wait(5)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertGreater(len(results_list_page.articles()), 1)

    #ADDED
    def test_search_only_with_what_but_with_focus_on_when_by_enter(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.search_where_input().send_keys(Keys.RETURN)
        webdriver.implicitly_wait(5)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertGreater(len(results_list_page.articles()), 1)

    #ADDED
    def test_search_only_with_where_when_yandex_found_greater_than_0(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        query = u"Москва"
        found_count = YandexAPI.get_found_count(query)
        self.assertGreater(found_count, 0)
        home_page.search_for_where(query)
        home_page.click_search_button()
        webdriver.implicitly_wait(5)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        self.assertGreater(len(results_list_page.articles()), 1, 'POI list is empty')

    #ADDED BUT NOT DONE
    def test_results_list_briefs(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.click_search_button()
        webdriver.implicitly_wait(5)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        results_list_page.get_results()

    #ADDED
    def test_locate_me_enter_valid_address(self):
        address = u'Москва, улица Жебрунова'
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.click_search_button()
        webdriver.implicitly_wait(10)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        results_list_page.click_search_locate_me()
        results_list_page.type_address(address)
        WebElementUtils.check_if_text_present_in_element_value(webdriver, (By.ID, LocateMe.lm_input_address_locator),
                                                               address)
        self.assertEqual(results_list_page.lm_input_address().get_attribute("value"), address)
        self.assertEqual(results_list_page.lm_location_enabled().text, address)
        self.assertFalse(results_list_page.lm_save_button_disabled().is_displayed(), 'save button is not present')
        self.assertTrue(results_list_page.lm_save_button_enabled().is_displayed(), 'save button is not present')
        results_list_page.click_save_location_button()
        self.assertEqual(results_list_page.search_where_input().get_attribute("value"), address)

    #ADDED
    def test_locate_me_move_pin(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.click_search_button()
        webdriver.implicitly_wait(10)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        results_list_page.click_search_locate_me()
        needed_text = u'Москва, улица Ильинка'
        past_inputted_text = results_list_page.lm_input_address().get_attribute("value")
        ActionChains(webdriver).drag_and_drop_by_offset(results_list_page.lm_map_pin(), 50, 50).perform()
        WebElementUtils.check_if_text_present_in_element_value(webdriver, (By.ID, LocateMe.lm_location_enabled_locator),
                                                               needed_text)
        present_inputted_text = results_list_page.lm_input_address().get_attribute("value")
        self.assertNotEqual(past_inputted_text, present_inputted_text)
        self.assertEqual(results_list_page.lm_location_enabled().text, present_inputted_text)

    #ADDED
    def test_locate_me_enter_unaccepted_address(self):
        needed_text = u'Адрес не найден, исправьте адрес или выберите место на карте мышкой'
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.click_search_button()
        webdriver.implicitly_wait(10)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        results_list_page.click_search_locate_me()
        results_list_page.type_address(u'UNACCEPTABLE')
        WebElementUtils.check_if_text_present_in_element_value(webdriver,
                                                               (By.ID, LocateMe.lm_location_disabled_locator),
                                                               needed_text)
        self.assertEqual(results_list_page.lm_location_disabled().text, needed_text)
        self.assertTrue(results_list_page.lm_save_button_disabled().is_displayed(), 'save button is present')
        self.assertFalse(results_list_page.lm_save_button_enabled().is_displayed(), 'save button is present')

    def test_distance_on_brief_card(self):
        where_query = u"Москва"
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_where(where_query)
        home_page.search_where_input().send_keys(Keys.RETURN)
        webdriver.implicitly_wait(5)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        results = results_list_page.get_results()
        items = SearchAPI().get_items('', where_query)
        for i, item in enumerate(items):
            self.assertTrue(round_distance(item['distanceInMeters']), results['pois'][i]['distance'])

    def test_quantity_of_objects(self):
        what_query = u"Бар"
        where_query = u"Москва"
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(what_query)
        home_page.search_for_where(where_query)
        home_page.click_search_button()
        webdriver.implicitly_wait(10)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        tc1 = results_list_page.total_count()
        tcbps1 = results_list_page.total_count_by_primary_search()
        stc1 = SearchAPI.get_total_count(what_query, where_query)
        stcbps1 = SearchAPI.get_total_count_by_primary_search(what_query, where_query)
        category_name = results_list_page.select_random_category()
        amenity_name = results_list_page.select_random_amenity()
        tc2 = results_list_page.total_count()
        tcbps2 = results_list_page.total_count_by_primary_search()
        stc2 = SearchAPI.get_total_count(what_query, where_query, categories=[category_name], amenities=[amenity_name])
        self.assertTrue(tcbps1, stcbps1)
        self.assertTrue(tc1, stc1)
        self.assertTrue(tc1, tcbps1)
        self.assertTrue(tc2, stc2)
        self.assertTrue(tcbps1, tcbps2)

    def test_sorting_by_distance_asc(self):
        what_query = u"Бар"
        where_query = u"Москва"
        sorting_type = u'geoDistance'
        sorting_direction = u'asc'
        webdriver = self.set_up_with_suffix(
            '#/result?what=' + what_query + '&where=' + where_query + '&sort=' + sorting_type + '&dir=' + sorting_direction)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        items = SearchAPI().get_items(what=what_query, where=where_query, sort_type=sorting_type,
                                      sort_dir=sorting_direction)
        names = results_list_page.articles_names()
        names_list = [x.text for x in names]
        item_names_list = [x[POI_KEYS.NAME] for x in items]
        self.assertListEqual(item_names_list, names_list)

    def test_sorting_by_distance_desc(self):
        what_query = u"Бар"
        where_query = u"Москва"
        sorting_type = u'geoDistance'
        sorting_direction = u'desc'
        webdriver = self.set_up_with_suffix(
            '#/result?what=' + what_query + '&where=' + where_query + '&sort=' + sorting_type + '&dir=' + sorting_direction)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        items = SearchAPI().get_items(what=what_query, where=where_query, sort_type=sorting_type,
                                      sort_dir=sorting_direction)
        names = results_list_page.articles_names()
        names_list = [x.text for x in names]
        item_names_list = [x[POI_KEYS.NAME] for x in items]
        self.assertListEqual(item_names_list, names_list)

    def test_back_to_search_results(self):
        what_query = u"Бар"
        where_query = u"Москва"
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(what_query)
        home_page.search_for_where(where_query)
        home_page.click_search_button()
        webdriver.implicitly_wait(10)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        results_list_page.select_random_category()
        results_list_page.select_random_amenity()
        results_list_page.select_random_cuisine()
        results_list_page.select_random_working_hours()
        results_list_page.select_random_metro_station()
        results_list_page.select_random_district()
        state1 = results_list_page.get_page_state()
        results_list_page.open_random_poi_page()
        poi_page = PageFactory.create_page(POIPage, webdriver)
        poi_page.click_back_to_search_results_button()
        time.sleep(3)
        state2 = results_list_page.get_page_state()
        self.assertDictEqual(state1, state2)
        pass


    def test_moscow_agglomeration(self):
        pass

        #def test_locate_me(self):
        #    webdriver = self.set_up()
        #    home_page = PageFactory.create_page(HomePage, webdriver)
        #    home_page.search_for_what(u"Бар")
        #    home_page.click_search_button()
        #    webdriver.implicitly_wait(10)
        #    results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        #    results_list_page.click_search_locate_me()
        #    results_list_page.click_locate_me()
        #    print '1'


if __name__ == "__main__":
    unittest.main()