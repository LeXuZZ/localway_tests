import unittest
from selenium.webdriver.support import wait
from selenium.webdriver.support.wait import WebDriverWait
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
        home_page.search_for_what("1223456")
        home_page.search_for_where("1223456")
        home_page.click_search_button()
        WebDriverWait(webdriver, 300)
        self.assertEqual(webdriver.title, "Localway")

if __name__ == "__main__":
    unittest.main()