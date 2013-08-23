# coding=utf-8
from decimal import Decimal
import time
from tests.pages import HomePage, ResultsListPage
from tests.utils.json_utils import SearchAPI
from tests.utils.mongo_utils import MongoDB
from tests.utils.weight_util import get_distance_real_weight, check_all_weight
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
        what_query = u'Бар'
        where_query = u'Москва Тверская 17'
        items = SearchAPI().get_items(what_query, where_query)
        for item in items:
            t = time.time()
            print 'POI name: ' + item['name'] + ' and id: ' + item['_id']
            poi = MongoDB().get_poi_by_id(item['_id'])
            fe_score = item['score']
            be_score = get_distance_real_weight(where_query, poi) + check_all_weight(what_query, poi)
            self.assertAlmostEqual(Decimal(fe_score).quantize(Decimal('1.00')), Decimal(be_score).quantize(Decimal('1.00')), 1)
            print (time.time()-t)

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
        item_names_list = [x['name'] for x in items]
        self.assertListEqual(item_names_list, names_list)