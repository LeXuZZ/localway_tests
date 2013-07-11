# coding=utf-8
import unittest
from nose.util import log
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
from tests.pages.results_list_page import ResultsList
from wtframework.wtf.web.page import PageFactory
from tests.pages.home_page import HomePage
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER

__author__ = 'lxz'


class LocalwayTest(WTFBaseTest):

    def test_home_page_basic(self):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get("http://172.31.237.12/")
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_what(u"Бар")
        home_page.search_for_where(u"Москва")
        home_page.click_search_button()
        webdriver.implicitly_wait(3000)
        results_list_page = PageFactory.create_page(ResultsList, webdriver)
        self.assertEqual(webdriver.title, "Localway")
        category = results_list_page.category_filter_list()
        category_path =  webdriver.execute_script("gPt=function(c){if(c.id!==''){return'id(\"'+c.id+'\")'}if(c===document.body){return c.tagName}var a=0;var e=c.parentNode.childNodes;for(var b=0;b<e.length;b++){var d=e[b];if(d===c){return gPt(c.parentNode)+'/'+c.tagName+'['+(a+1)+']'}if(d.nodeType===1&&d.tagName===c.tagName){a++}}};return gPt(arguments[0]).toLowerCase();", category)
        print category_path
        print('test ok')

if __name__ == "__main__":
    unittest.main()