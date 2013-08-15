import unittest
from tests.pages.poi_page import POIPage
from tests.static.constants import URL_PREFIXES
from tests.utils.data_utils import crop_first_zero_if_exist, convert_ms_to_HM, get_digits_from_string
from wtframework.wtf.utils.json_utils import POI_JSON
from wtframework.wtf.web.page import PageFactory
from tests.utils.mongo_utils import MongoDB
from wtframework.wtf.config import ConfigReader
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER

__author__ = 'lxz'


class POIPageTest(WTFBaseTest):

    maxDiff = None

    def set_up(self):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(ConfigReader('site_credentials').get("default_url"))
        return webdriver

    def test_yandex_map_existence_true_scenario(self):
        poi_id_with_yandex_map = MongoDB().get_random_poi_with_existing_coordinates()['_id']
        webdriver = self.set_up()
        webdriver.get(ConfigReader('site_credentials').get("default_url") + URL_PREFIXES.POI_ID_PREFIX + str(poi_id_with_yandex_map))
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        self.assertIsNotNone(POI_JSON(str(poi_id_with_yandex_map)).lat)
        self.assertIsNotNone(POI_JSON(str(poi_id_with_yandex_map)).lon)
        self.assertTrue(poi_page.yandex_map().is_displayed())

    def test_yandex_map_existence_false_scenario(self):
        poi_id_without_yandex_map = MongoDB().get_random_poi_without_existing_coordinates()['_id']
        webdriver = self.set_up()
        webdriver.get(ConfigReader('site_credentials').get("default_url") + URL_PREFIXES.POI_ID_PREFIX + str(poi_id_without_yandex_map))
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        self.assertIsNone(POI_JSON(str(poi_id_without_yandex_map)).lat)
        self.assertIsNone(POI_JSON(str(poi_id_without_yandex_map)).lon)
        self.assertFalse(poi_page.yandex_map().is_displayed())

    def test_cuisine_is_shown(self):
        random_poi_id_with_cuisines = MongoDB().get_random_poi_with_cuisines()['_id']
        webdriver = self.set_up()
        webdriver.get(
            ConfigReader('site_credentials').get("default_url") + URL_PREFIXES.POI_ID_PREFIX + str(random_poi_id_with_cuisines))
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        self.assertGreater(len(poi_page.cuisines()), 0, "block cuisines does not exist")

    def test_cuisine_is_not_shown(self):
        random_poi_id_without_cuisines = MongoDB().get_random_poi_without_cuisines()['_id']
        webdriver = self.set_up()
        webdriver.get(
            ConfigReader('site_credentials').get("default_url") + URL_PREFIXES.POI_ID_PREFIX + str(random_poi_id_without_cuisines))
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        self.assertEqual(len(poi_page.cuisines()), 0, "block cuisines does exist")

    def test_hotel_stars_and_check_io_is_shown(self):
        poi_with_hotel_stars_and_check_io = MongoDB().get_random_poi_with_hotel_stars_greater_than_0_and_check_io()
        poi_id = poi_with_hotel_stars_and_check_io['_id']
        hotel_stars_count_in_mongo = poi_with_hotel_stars_and_check_io['hotelStars']
        checkin_time_in_mongo = crop_first_zero_if_exist(
            convert_ms_to_HM(poi_with_hotel_stars_and_check_io['checkinTime']))
        checkout_time_in_mongo = crop_first_zero_if_exist(
            convert_ms_to_HM(poi_with_hotel_stars_and_check_io['checkoutTime']))
        webdriver = self.set_up()
        webdriver.get(ConfigReader('site_credentials').get("default_url") + URL_PREFIXES.POI_ID_PREFIX + str(
            poi_id))
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        hotel_stars_count_on_ui = get_digits_from_string(poi_page.hotel_stars().get_attribute('class'))
        self.assertEqual(hotel_stars_count_in_mongo, hotel_stars_count_on_ui, 'hotel stars count different')
        self.assertEqual(checkin_time_in_mongo, poi_page.checkin_time().text)
        self.assertEqual(checkout_time_in_mongo, poi_page.checkout_time().text)

    def test_hotel_stars_is_not_shown_and_check_io_is_shown(self):
        poi_without_hotel_stars_and_check_io = MongoDB().get_random_poi_with_hotel_stars_equals_0_and_check_io_gt_0()
        poi_id = poi_without_hotel_stars_and_check_io['_id']
        checkin_time_in_mongo = crop_first_zero_if_exist(
            convert_ms_to_HM(poi_without_hotel_stars_and_check_io['checkinTime']))
        checkout_time_in_mongo = crop_first_zero_if_exist(
            convert_ms_to_HM(poi_without_hotel_stars_and_check_io['checkoutTime']))
        webdriver = self.set_up()
        webdriver.get(ConfigReader('site_credentials').get("default_url") + URL_PREFIXES.POI_ID_PREFIX + str(
            poi_id))
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        self.assertEqual('stars', poi_page.hotel_stars().get_attribute('class'))
        self.assertEqual(checkin_time_in_mongo, poi_page.checkin_time().text)
        self.assertEqual(checkout_time_in_mongo, poi_page.checkout_time().text)

if __name__ == "__main__":
    unittest.main()