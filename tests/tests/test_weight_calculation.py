# coding=utf-8
from decimal import Decimal
import time
from tests.pages import HomePage, ResultsListPage
from tests.static.constants import WEIGHT, POI_KEYS
from tests.utils.json_utils import SearchAPI, ElasticSearchAPI, YandexAPI
from tests.utils.mongo_utils import MongoDB
from tests.utils.weight_util import get_distance_real_weight, check_all_weight, distance
from wtframework.wtf.web.page import PageFactory
from wtframework.wtf.config import ConfigReader
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER

__author__ = 'lxz'


class WeightTest(WTFBaseTest):

    maxDiff = None

    def set_up(self):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(ConfigReader('site_credentials').get("default_url"))
        return webdriver

    def test_weight_calculate(self):
        what_query = u'парк разв'
        where_query = u'Тверская'
        items = SearchAPI().get_items(what_query, where_query)
        for item in items:
            # t = time.time()
            # print 'POI name: ' + item[POI_KEYS.NAME] + ' and id: ' + item[POI_KEYS.ID]
            es_poi_street_point = ElasticSearchAPI().get_poi_json(item['_id'])['streetPoint']
            where_coordinates = YandexAPI.get_coordinates(where_query)
            if distance(float(es_poi_street_point[POI_KEYS.LATITUDE]), float(es_poi_street_point[POI_KEYS.LONGITUDE]), float(where_coordinates[POI_KEYS.LATITUDE]), float(where_coordinates[POI_KEYS.LONGITUDE])) < 10:
                N = WEIGHT.STREET_NEAR_COOF
            else:
                N = WEIGHT.STREET_NOT_NEAR_COOF
            poi = MongoDB().get_poi_by_id(item[POI_KEYS.ID])
            fe_score = item[POI_KEYS.SCORE]
            be_score = get_distance_real_weight(where_query, poi, N) + check_all_weight(what_query, poi)
            print item['name']
            print Decimal(fe_score).quantize(Decimal('1.00'))
            print Decimal(be_score).quantize(Decimal('1.00'))
            self.assertAlmostEqual(Decimal(fe_score).quantize(Decimal('1.00')), Decimal(be_score).quantize(Decimal('1.00')), 1)
            # print (time.time()-t)

    def test_weight_ranging_view(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        what_query = u"Бар"
        where_query = u'Москва Тверская 17'
        home_page.search_for_what(what_query)
        home_page.search_for_where(where_query)
        home_page.click_search_button()
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        items = SearchAPI().get_items(what_query, where_query)
        names = results_list_page.articles_names()
        names_list = [x.text for x in names]
        item_names_list = [x[POI_KEYS.NAME] for x in items]
        self.assertListEqual(item_names_list, names_list)