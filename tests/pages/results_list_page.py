import re
from selenium.webdriver.common.keys import Keys
from wtframework.wtf.web.webelement import WebElementUtils
from tests.pages.block_objects import HeaderBlock, FooterBlock, ResultsListPOIBrief, LocateMe, SearchBlock
from wtframework.wtf.web.page import PageObject, InvalidPageError

__author__ = 'lxz'


class ResultsListPage(PageObject, HeaderBlock, FooterBlock, ResultsListPOIBrief, LocateMe, SearchBlock):


    articles_xpath = '//section[@class="result-items"]/a/div[1]'
    name_xpath_pref = '/section/span/h4'
    ### Page Elements Section ###
    categories_checked = lambda self: self.webdriver.find_elements_by_xpath('//aside/section[1]/div/ul[1]/li')
    categories_unchecked = lambda self: self.webdriver.find_elements_by_xpath('//aside/section[1]/div/ul[2]/li')
    # category_filter_list = lambda self: self.webdriver.find_element_by_xpath("//aside/section[1]/div/ul[1]/li")
    amenities_checked = lambda self: self.webdriver.find_elements_by_xpath('//aside/section[2]/div/ul[1]/li')
    amenities_unchecked = lambda self: self.webdriver.find_elements_by_xpath('//aside/section[2]/div/ul[2]/li')
    # amenity_filter_list = lambda self: self.webdriver.find_element_by_class_name("amenity_filter_list")
    cuisines_checked = lambda self: self.webdriver.find_elements_by_xpath('//aside/section[3]/div/ul[1]/li')
    cuisines_unchecked = lambda self: self.webdriver.find_elements_by_xpath('//aside/section[3]/div/ul[2]/li')
    # cuisine_filter_list = lambda self: self.webdriver.find_element_by_class_name("cuisine_filter_list")
    district_filter_list = lambda self: self.webdriver.find_element_by_class_name('district_filter_list')
    metro_station_filter_list = lambda self: self.webdriver.find_element_by_class_name('metro_station_filter_list')
    schedule_filter_list = lambda self: self.webdriver.find_element_by_class_name('schedule_filter_list')
    poi_place_holder = lambda self: self.webdriver.find_element_by_class_name('poi_placeholder')
    poi_list = lambda self: self.webdriver.find_element_by_xpath('//section[@class="result-items"]')
    articles = lambda self: self.webdriver.find_elements_by_xpath(self.articles_xpath)
    articles_names = lambda self: self.webdriver.find_elements_by_xpath(self.articles_xpath + self.name_xpath_pref)
    pagination_panel = lambda self: self.webdriver.find_element_by_class_name("pagination")





    ### End Page Elements Section ###

    def _validate_page(self, webdriver):

        '''
        Validates we are on the correct page.
        '''

        if not re.search('Localway', webdriver.title):
            raise InvalidPageError('This page did not pass ResultsListPage page validation.')

    def type_address(self, address_string):
        self.lm_input_address().clear()
        self.webdriver.implicitly_wait(3)
        self.lm_input_address().send_keys(address_string)
        self.lm_input_address().send_keys(Keys.RETURN)

    def click_locate_me(self):
        WebElementUtils.check_is_displayed(self.webdriver, self.lm_locate_me_button())
        self.lm_locate_me_button().click()

    def click_save_location_button(self):
        WebElementUtils.check_is_displayed(self.webdriver, self.lm_save_button_enabled())
        self.lm_save_button_enabled().click()

    def click_search_locate_me(self):
        self.search_locate_me_button().click()
        WebElementUtils.check_if_attached_in_dom(self.webdriver, self.lm_input_address())