import re

__author__ = 'lxz'

from wtframework.wtf.web.page import PageObject, InvalidPageError


class POIPage(PageObject):
    '''
    POIPage
    WTFramework PageObject representing a page like:
    http://172.31.237.12/
    '''


    ### Page Elements Section ###
    yandex_map = lambda self: self.webdriver.find_element_by_xpath(
        "//*[@class=\"location\"]/div[@class=\"map\"]")
    categories = lambda self: self.webdriver.find_elements_by_xpath("//*[@data-bind=\"amenities\"]/div/a")
    cuisines = lambda self: self.webdriver.find_elements_by_xpath("//*[@data-bind=\"cuisines\"]/div/a")
    check_in_time = lambda self: self.webdriver.find_element_by_xpath("//*[@data-bind=\"checkinTime\"]")
    check_out_time = lambda self: self.webdriver.find_element_by_xpath("//*[@data-bind=\"checkoutTime\"]")
    ### End Page Elements Section ###

    def _validate_page(self, webdriver):

        if not re.search("Localway", webdriver.title):
            raise InvalidPageError("This page did not pass POIPage page validation.")
