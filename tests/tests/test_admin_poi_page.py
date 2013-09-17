# coding=utf-8
from tests.utils.postgre_utils import PostgreSQL
from wtframework.wtf.web.page import PageFactory
from tests.pages.admin_poi_page import AdminPOIPage
from tests.static.constants import URL_PREFIXES
from wtframework.wtf.config import ConfigReader
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER

__author__ = 'lxz'


class AdminPOIPageTest(WTFBaseTest):
    maxDiff = None

    def set_up(self):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(ConfigReader('site_credentials').get("admin_url"))
        return webdriver

    def set_up_with_suffix(self, suffix):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(ConfigReader('site_credentials').get("admin_url") + suffix)
        return webdriver

    def test_admin_poi_page(self):
        webdriver = self.set_up_with_suffix(URL_PREFIXES.ADMIN_POI_ID_PREFIX + '173760')
        webdriver.implicitly_wait(10)
        admin_poi_page = PageFactory.create_page(AdminPOIPage, webdriver)
        payments = admin_poi_page.get_payments()
        name = admin_poi_page.get_name()
        admin_poi_page.select_section(u'Достопримечательности')
        admin_poi_page.select_region(u'Московская область')
        admin_poi_page.select_status(u'Архив')

    def test_object_block(self):
        place_id = '168477'
        pg = PostgreSQL()
        webdriver = self.set_up_with_suffix(URL_PREFIXES.ADMIN_POI_ID_PREFIX + place_id)
        webdriver.implicitly_wait(10)
        poi_info = pg.get_current_revision_info_by_place_id(place_id)
        admin_poi_page = PageFactory.create_page(AdminPOIPage, webdriver)
        region_name = pg.get_region_name_by_place_id(place_id)
        region_short_name = pg.get_prefix_name_by_city_id(poi_info['city_id'])
        self.assertEqual(admin_poi_page.get_name(), poi_info['name'].decode("utf-8"))
        self.assertEqual(admin_poi_page.get_current_section(), u'Дети')
        self.assertEqual(admin_poi_page.get_current_category(), u'')
        self.assertEqual(admin_poi_page.get_categories(), pg.get_category_names_and_priorities_by_place_id(place_id))

        self.assertEqual(admin_poi_page.get_current_region(), region_name.decode("utf-8") + ' ' + region_short_name.decode("utf-8").lower())
        self.assertEqual(admin_poi_page.get_current_city(), pg.get_prefix_short_name_by_city_id(poi_info['city_id']).decode("utf-8") + ' ' + pg.get_city_name_by_city_id(poi_info['city_id']).decode("utf-8"))
        self.assertEqual(admin_poi_page.get_street(), poi_info['street'].decode("utf-8"))
        self.assertEqual(admin_poi_page.get_house(), poi_info['house'].decode("utf-8"))
        self.assertEqual(admin_poi_page.get_building(), poi_info['building'].decode("utf-8"))
        self.assertEqual(admin_poi_page.get_metro_names(), pg.get_metro_names_by_place_id(place_id))