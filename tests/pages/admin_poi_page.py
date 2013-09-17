# coding=utf-8
from collections import defaultdict
import re
from selenium.webdriver.support.select import Select
from wtframework.wtf.web.page import PageObject, InvalidPageError

__author__ = 'lxz'


class AdminPOIPage(PageObject):

    def _validate_page(self, webdriver):
        if not re.search('Localway admin', webdriver.title):
            raise InvalidPageError("This page did not pass AdminPOIPage page validation.")

    #Object

    name_loc = 'inputName'
    section_loc = 'input-section'
    category_loc = 'input-category'
    categories_loc = './/span[@data-bind="category"]'
    region_loc = 'input-region'
    city_loc = 'input-city'
    street_loc = 'input-street'
    house_loc = 'input-house'
    building_loc = 'input-building'
    metro_loc = 'input-metro'

    def _name(self):
        return self.webdriver.find_element_by_id(self.name_loc)

    def get_name(self):
        return self._name().get_attribute('value')

    def set_name(self, text):
        self._name().clear()
        self.webdriver.implicitly_wait(3)
        self._name().send_keys(text)

    def _section(self):
        return self.webdriver.find_element_by_id(self.section_loc)

    def select_section(self, text_):
        select = Select(self.webdriver.find_element_by_id(self.section_loc))
        select.select_by_visible_text(text_)

    def get_current_section(self):
        return Select(self.webdriver.find_element_by_id(self.section_loc)).first_selected_option.text

    def _category(self):
        return self.webdriver.find_element_by_id(self.category_loc)

    def type_category(self, text):
        self._category().clear()
        self.webdriver.implicitly_wait(3)
        self._category().send_keys(text)

    def get_current_category(self):
        return self._category().get_attribute('value')

    def _categories(self, shelf):
        return shelf.find_elements_by_xpath(self.categories_loc)

    def get_categories(self):
        categories = []
        shelves = self.get_category_shelves()
        for i in range(len(shelves)):
            categories.append([x.text for x in self._categories(shelves[i])])
        cat = []
        for i in range(len(categories)):
            for j in range(len(categories[i])):
                cat.append(dict(name=categories[i][j], priority=i + 1))
        return cat

    def get_category_shelves(self):
        return self.webdriver.find_elements_by_xpath('//tr[@data-bind="categoryShelf"]')

    def _region_dropdown(self):
        return self.webdriver.find_element_by_id(self.region_loc)

    def select_region(self, text_):
        Select(self._region_dropdown()).select_by_visible_text(text_)

    def get_current_region(self):
        return Select(self._region_dropdown()).first_selected_option.text

    def _city(self):
        return self.webdriver.find_element_by_id(self.city_loc)

    def type_city(self, text):
        self._city().clear()
        self.webdriver.implicitly_wait(3)
        self._city().send_keys(text)

    def get_current_city(self):
        return self._city().get_attribute('value')

    def _street(self):
        return self.webdriver.find_element_by_id(self.street_loc)

    def type_street(self, text):
        self._street().clear()
        self.webdriver.implicitly_wait(3)
        self._street().send_keys(text)

    def get_street(self):
        return self._street().get_attribute('value')

    def _house(self):
        return self.webdriver.find_element_by_id(self.house_loc)

    def type_house(self, text):
        self._house().clear()
        self.webdriver.implicitly_wait(3)
        self._house().send_keys(text)

    def get_house(self):
        return self._house().get_attribute('value')

    def _building(self):
        return self.webdriver.find_element_by_id(self.building_loc)

    def type_building(self, text):
        self._building().clear()
        self.webdriver.implicitly_wait(3)
        self._building().send_keys(text)

    def get_building(self):
        return self._building().get_attribute('value')

    def _metro(self):
        return self.webdriver.find_element_by_id(self.metro_loc)

    def metro_names(self):
        return self.webdriver.find_elements_by_xpath('//span[@data-bind="metroName"]')

    def get_metro_names(self):
        return [x.text for x in self.metro_names()]

    #Description
    intro_input = lambda self: self.webdriver.find_element_by_id('intro-input')
    description_input = lambda self: self.webdriver.find_element_by_id('intro-description')

    #Other
    editor_choice = lambda self: self.webdriver.find_elements_by_xpath('//input[@data-bind="editorChoice"]')

    #Payments
    payments_checkboxes = lambda self: self.webdriver.find_elements_by_xpath('//input[@data-bind="payment"]')
    payments_names = lambda self: self.webdriver.find_elements_by_xpath('//input[@data-bind="payment"]/following-sibling::span')

    def get_payments(self):
        payments = []
        payments_names_text = [x.text for x in self.payments_names()]
        pc = self.payments_checkboxes()
        for i in range(len(payments_names_text)):
            is_checked = pc[i].is_selected()
            payments.append([payments_names_text[i], pc[i], is_checked])
        return payments

    #Tags
    def tags_input(self):
        return self.webdriver.find_element_by_id('input-tags')

    #Status
    def select_status(self, text_):
        select = Select(self.webdriver.find_element_by_id("input-status"))
        select.select_by_visible_text(text_)

    def get_status(self):
        return Select(self.webdriver.find_element_by_id("input-status")).first_selected_option.text

    #Map
    def _lat(self):
        return self.webdriver.find_element_by_id('txtLat')

    def get_lat(self):
        return self._lat().get_attribute('value')

    def _lon(self):
        return self.webdriver.find_element_by_id('txtLon')

    def get_lon(self):
        return self._lon().get_attribute('value')

    #Notes
    def _notes(self):
        return self.webdriver.find_element_by_id('notes')

    def type_notes(self, text):
        self._notes().clear()
        self.webdriver.implicitly_wait(3)
        self._notes().send_keys(text)

    def get_notes(self):
        return self._notes().get_attribute('value')
