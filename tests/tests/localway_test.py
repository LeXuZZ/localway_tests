# coding=utf-8
import unittest
from wtframework.wtf.config import ConfigReader
from tests.pages.results_list_page import ResultsList
from wtframework.wtf.utils.json_utils import POI_JSON
from wtframework.wtf.utils.mongo_utils import MongoDB
from wtframework.wtf.web.page import PageFactory, PageUtils
from tests.pages.home_page import HomePage
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER
__author__ = 'lxz'


class LocalwayTest(WTFBaseTest):

    def test_home_page_basic(self):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(ConfigReader('site_credentials').get("default_url"))
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.search_for_where(u"Москва")
        home_page.click_search_button()
        webdriver.implicitly_wait(3000)
        results_list_page = PageFactory.create_page(ResultsList, webdriver)
        self.assertEqual(webdriver.title, "Localway")
        category = results_list_page.category_filter_list()
        category_path = PageUtils.get_element_xpath(category)
        print category_path
        print('test ok')

    def json_test(self):
        a = POI_JSON("161606af0000000000000000")
        b = MongoDB()
        print '1'

if __name__ == "__main__":
    unittest.main()