import unittest
from tests.pages.poi_page import POIPage
from tests.static.constants import POI_KEYS, URL_PREFIXES
from wtframework.wtf.testobjects.test_decorators import ddt, csvdata
from tests.utils.data_utils import delete_newlines_for_description_and_intro, get_digits_from_string, create_address_from_poi, create_dict_for_contacts, convert_working_time_from_poi, convert_average_price_from_poi, convert_business_lunch_from_poi, get_image_id_from_src, convert_metro_station
from wtframework.wtf.web.page import PageFactory
from wtframework.wtf.config import ConfigReader
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from tests.utils.mongo_utils import MongoDB
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER

__author__ = 'lxz'

@ddt
class DDTPOIPageTest(WTFBaseTest):
    maxDiff = None

    def set_up(self):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(ConfigReader('site_credentials').get("default_url"))
        return webdriver

    def set_up_with_suffix(self, suffix):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(ConfigReader('site_credentials').get("default_url") + suffix)
        return webdriver

    def generate_pois_id(self):
        for i in range(10):
            poi = MongoDB().get_random_poi()
            return poi['_id']

    #AWLOCALWAY-503
    @csvdata("testdata.csv")
    def test_complex_check_poi_page(self, paramater_dic):
        poi = MongoDB().get_poi_by_id(paramater_dic['poi_id'])
        webdriver = self.set_up_with_suffix(URL_PREFIXES.POI_ID_PREFIX + paramater_dic['poi_id'])
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
            #check name
        if POI_KEYS.NAME in poi.keys():
            self.assertEqual(poi[POI_KEYS.NAME], poi_page.name().text)
            #check description
        if POI_KEYS.DESCRIPTION in poi.keys():
            self.assertEqual(delete_newlines_for_description_and_intro(poi[POI_KEYS.DESCRIPTION]),
                             poi_page.description().text)
            #check intro
        if POI_KEYS.INTRO in poi.keys():
            self.assertEqual(delete_newlines_for_description_and_intro(poi[POI_KEYS.INTRO]), poi_page.intro().text)
            #check rating stars and rating number
        if POI_KEYS.RATING in poi.keys():
            self.assertEqual(poi[POI_KEYS.RATING],
                             float(get_digits_from_string(poi_page.rating_stars().get_attribute('class'))))
            self.assertEqual(poi[POI_KEYS.RATING], float(poi_page.rating().text))
            #check address (containing city, street, building, house)
        if any(c in poi.keys() for c in [POI_KEYS.CITY, POI_KEYS.STREET, POI_KEYS.BUILDING, POI_KEYS.HOUSE]):
            self.assertEqual(create_address_from_poi(poi), poi_page.address().text)
            #check image
        if POI_KEYS.IMAGES in poi.keys():
            if poi[POI_KEYS.IMAGES]:
                self.assertTrue(poi_page.gallery_main().is_displayed())
            else:
                self.assertFalse(poi_page.gallery_main().is_displayed())
            #check categories
        if POI_KEYS.CATEGORIES in poi.keys():
            self.assertEqual(MongoDB().get_categories(poi), poi_page.get_categories())
            #check amenities
        if POI_KEYS.AMENITIES in poi.keys():
            self.assertEqual(MongoDB().get_amenities(poi), poi_page.get_amenities())
            #check metro stations
        if POI_KEYS.METRO_STATIONS in poi.keys():
            self.assertEqual(MongoDB().get_metro_stations(poi), poi_page.get_metro_stations())
            #check payments
        if POI_KEYS.PAYMENTS in poi.keys():
            self.assertEqual(MongoDB().get_payments(poi), poi_page.get_payments())
            #check contacts
        if POI_KEYS.CONTACTS in poi.keys():
            self.assertDictEqual(create_dict_for_contacts(poi), poi_page.get_contacts_dict())
            #check work time
        if POI_KEYS.WORK_TIME in poi.keys():
            self.assertEqual(convert_working_time_from_poi(poi), poi_page.get_worktime())
            #check average price
        if POI_KEYS.AVERAGE_PRICE in poi.keys():
            if poi[POI_KEYS.AVERAGE_PRICE]:
                self.assertEqual(convert_average_price_from_poi(poi), poi_page.average_price().text)
            #check business lunch price
        if POI_KEYS.BUSINESS_LUNCH_PRICE in poi.keys():
            if poi[POI_KEYS.BUSINESS_LUNCH_PRICE]:
                self.assertEqual(convert_business_lunch_from_poi(poi), poi_page.business_lunch().text)
            #check cuisines
        if POI_KEYS.CUISINES in poi.keys():
            self.assertEqual(MongoDB().get_cuisines(poi), poi_page.get_cuisines())
            #check map existence
        if POI_KEYS.LONGITUDE in poi.keys() and POI_KEYS.LONGITUDE in poi.keys():
            self.assertTrue(poi_page.yandex_map().is_displayed())
        else:
            self.assertFalse(poi_page.yandex_map().is_displayed())


if __name__ == "__main__":
    unittest.main()