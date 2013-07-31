import re
from wtframework.wtf.web.page import PageObject, InvalidPageError

__author__ = 'lxz'


class ResultsList(PageObject):


    ### Page Elements Section ###
    category_filter_list = lambda self: self.webdriver.find_element_by_class_name("category_filter_list")
    amenity_filter_list = lambda self: self.webdriver.find_element_by_class_name("amenity_filter_list")
    cuisine_filter_list = lambda self: self.webdriver.find_element_by_class_name("cuisine_filter_list")
    district_filter_list = lambda self: self.webdriver.find_element_by_class_name("district_filter_list")
    metro_station_filter_list = lambda self: self.webdriver.find_element_by_class_name("metro_station_filter_list")
    schedule_filter_list = lambda self: self.webdriver.find_element_by_class_name("schedule_filter_list")
    search_what_input = lambda self: self.webdriver.find_element_by_xpath("/html/body/div/form/input")
    search_where_input = lambda self: self.webdriver.find_element_by_xpath("/html/body/div/form/input[2]")
    search_button = lambda self: self.webdriver.find_element_by_xpath("/html/body/div/form/button")
    poi_place_holder = lambda self: self.webdriver.find_element_by_class_name("poi_placeholder")
    poi_list = lambda self: self.webdriver.find_element_by_xpath("//section[@class=\"result-items\"]")
    poi_list_articles = lambda self: self.webdriver.find_elements_by_xpath("//*[@class=\"result-items\"]/article")
    pagination_panel = lambda self: self.webdriver.find_element_by_class_name("pagination")

    ### End Page Elements Section ###

    def _validate_page(self, webdriver):

        '''
        Validates we are on the correct page.
        '''

        if not re.search('Localway', webdriver.title):
            raise InvalidPageError('This page did not pass ResultsListPage page validation.')

