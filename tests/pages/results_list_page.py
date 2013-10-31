# coding=utf-8
from random import choice
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from wtframework.wtf.web.webelement import WebElementUtils, text_to_be_present_in_one_of_elements
from tests.pages.block_objects import HeaderBlock, FooterBlock, ResultsListPOIBrief, LocateMe, SearchBlock
from wtframework.wtf.web.page import PageObject, InvalidPageError
from selenium.webdriver.support import expected_conditions as EC

__author__ = 'lxz'


class ResultsListPage(PageObject, HeaderBlock, FooterBlock, ResultsListPOIBrief, LocateMe, SearchBlock):
    sorting_dropdown_loc = '/html/body/section[1]/section/section[2]/section/section/header/div[2]/div[1]/a'

    articles_xpath = '//section[@class="result-items"]/a/div[1]'
    name_xpath_pref = '/section/span/h4'
    ### Page Elements Section ###
    categories_checked = lambda self: self.webdriver.find_elements_by_xpath(
        u'//h6[contains(text(),"Категории")]/parent::node()/ul[1]/li/div/input[count(@disabled)=0]/../label')
    categories_unchecked = lambda self: self.webdriver.find_elements_by_xpath(
        u'//h6[contains(text(),"Категории")]/parent::node()/ul[2]/li/div/input[count(@disabled)=0]/../label')
    # category_filter_list = lambda self: self.webdriver.find_element_by_xpath("//aside/section[1]/div/ul[1]/li")
    amenities_checked = lambda self: self.webdriver.find_elements_by_xpath(
        u'//h6[contains(text(),"Услуги")]/parent::node()/ul[1]/li/div/input[count(@disabled)=0]/../label')
    amenities_unchecked = lambda self: self.webdriver.find_elements_by_xpath(
        u'//h6[contains(text(),"Услуги")]/parent::node()/ul[2]/li/div/input[count(@disabled)=0]/../label')
    # amenity_filter_list = lambda self: self.webdriver.find_element_by_class_name("amenity_filter_list")
    cuisines_checked = lambda self: self.webdriver.find_elements_by_xpath(
        u'//h6[contains(text(),"Кухни")]/parent::node()/ul[1]/li/div/input[count(@disabled)=0]/../label')
    cuisines_unchecked = lambda self: self.webdriver.find_elements_by_xpath(
        u'//h6[contains(text(),"Кухни")]/parent::node()/ul[2]/li/div/input[count(@disabled)=0]/../label')
    # cuisine_filter_list = lambda self: self.webdriver.find_element_by_class_name("cuisine_filter_list")
    districts_checked = lambda self: self.webdriver.find_elements_by_xpath(
        u'//h6[contains(text(),"Районы")]/parent::node()/ul[1]/li/div/input[count(@disabled)=0]/../label')
    districts_unchecked = lambda self: self.webdriver.find_elements_by_xpath(
        u'//h6[contains(text(),"Районы")]/parent::node()/ul[2]/li/div/input[count(@disabled)=0]/../label')
    #district_filter_list = lambda self: self.webdriver.find_element_by_class_name('district_filter_list')
    metro_stations_checked = lambda self: self.webdriver.find_elements_by_xpath(
        u'//h6[contains(text(),"Станции метро")]/parent::node()/ul[1]/li/div/input[count(@disabled)=0]/../label')
    metro_stations_unchecked = lambda self: self.webdriver.find_elements_by_xpath(
        u'//h6[contains(text(),"Станции метро")]/parent::node()/ul[2]/li/div/input[count(@disabled)=0]/../label')
    #metro_station_filter_list = lambda self: self.webdriver.find_element_by_class_name('metro_station_filter_list')
    working_hours_checked = lambda self: self.webdriver.find_elements_by_xpath(
        u'//h6[contains(text(),"Время работы")]/parent::node()/ul[2]//input[@checked="checked"]/../../div/input[count(@disabled)=0]/../label')
    working_hours_unchecked = lambda self: self.webdriver.find_elements_by_xpath(
        u'//h6[contains(text(),"Время работы")]/parent::node()/ul[2]/li/div/input[count(@disabled)=0]/../label')
    #schedule_filter_list = lambda self: self.webdriver.find_element_by_class_name('schedule_filter_list')
    poi_place_holder = lambda self: self.webdriver.find_element_by_class_name('poi_placeholder')
    poi_list = lambda self: self.webdriver.find_element_by_xpath('//section[@class="result-items"]')
    articles = lambda self: self.webdriver.find_elements_by_xpath(self.articles_xpath)
    articles_names = lambda self: self.webdriver.find_elements_by_xpath(self.articles_xpath + self.name_xpath_pref)
    pagination_panel = lambda self: self.webdriver.find_element_by_class_name('pagination')
    total_count = lambda self: self.webdriver.find_element_by_id('totalCount').text
    total_count_by_primary_search = lambda self: self.webdriver.find_element_by_id('totalCountByPrimarySearch').text
    back_to_search_button = lambda self: self.webdriver.find_element_by_id('backToSearchButton')
    current_sorting = lambda self: self.webdriver.find_element_by_id('sortingCurrent')

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

    def click_back_to_search_results_button(self):
        self.back_to_search_button().click()

    def get_page_state(self):
        total_count = self.total_count()
        total_count_by_primary_search = self.total_count_by_primary_search()
        names_list = [x.text for x in self.articles_names()]
        checked_categories = [x.text for x in self.categories_checked()]
        checked_amenities = [x.text for x in self.amenities_checked()]
        checked_cuisines = [x.text for x in self.cuisines_checked()]
        checked_working_hours = [x.text for x in self.working_hours_checked()]
        checked_metro_stations = [x.text for x in self.metro_stations_checked()]
        checked_districts = [x.text for x in self.districts_checked()]
        current_sorting = self.current_sorting().text
        return dict(total_count=total_count, total_count_by_primary_search=total_count_by_primary_search,
                    names_list=names_list, checked_categories=checked_categories, checked_amenities=checked_amenities,
                    checked_cuisines=checked_cuisines, checked_working_hours=checked_working_hours,
                    checked_metro_stations=checked_metro_stations, checked_districts=checked_districts,
                    current_sorting=current_sorting)

    def select_random_amenity(self):
        amenity = choice(self.amenities_unchecked())
        amenity_text = amenity.text
        amenity.click()
        amenities = [x for x in self.amenities_checked()]
        WebDriverWait(self.webdriver, 10).until(text_to_be_present_in_one_of_elements(amenities, amenity_text))
        return amenity_text

    def select_random_category(self):
        category = choice(self.categories_unchecked())
        category_text = category.text
        category.click()
        categories = [x for x in self.categories_checked()]
        WebDriverWait(self.webdriver, 10).until(text_to_be_present_in_one_of_elements(categories, category_text))
        return category_text

    def select_random_cuisine(self):
        cu = self.cuisines_unchecked()
        if cu:
            cuisine = choice(cu)
            cuisine_text = cuisine.text
            cuisine.click()
            cuisines = [x for x in self.cuisines_checked()]
            WebDriverWait(self.webdriver, 10).until(text_to_be_present_in_one_of_elements(cuisines, cuisine_text))
            return cuisine_text
        else:
            return None

    def select_random_working_hours(self):
        working_hours = choice(self.working_hours_unchecked())
        working_hours_text = working_hours.text
        working_hours.click()
        working_hours_all = [x for x in self.working_hours_checked()]
        WebDriverWait(self.webdriver, 10).until(text_to_be_present_in_one_of_elements(working_hours_all, working_hours_text))
        return working_hours_text

    def select_random_metro_station(self):
        metro_stations = choice(self.metro_stations_unchecked())
        metro_stations_text = metro_stations.text
        metro_stations.click()
        metro_stations_all = [x for x in self.metro_stations_checked()]
        WebDriverWait(self.webdriver, 10).until(text_to_be_present_in_one_of_elements(metro_stations_all, metro_stations_text))
        return metro_stations_text

    def select_random_district(self):
        districts = choice(self.districts_unchecked())
        districts_text = districts.text
        districts.click()
        districts_all = [x for x in self.districts_checked()]
        WebDriverWait(self.webdriver, 10).until(text_to_be_present_in_one_of_elements(districts_all, districts_text))
        return districts_text


def check_element_with_text_presence(text, elements_list):
    if text in [x.text for x in elements_list]:
        return True
    else:
        return False


    #def _sorting_dropdown(self):
    #    return self.webdriver.find_element_by_xpath(self.sorting_dropdown_loc)
    #
    #def select_sorting(self, text_):
    #    Select(self._sorting_dropdown()).select_by_visible_text(text_)
    #
    #def get_current_sorting(self):
    #    return Select(self._sorting_dropdown()).first_selected_option.text