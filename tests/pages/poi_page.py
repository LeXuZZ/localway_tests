# coding=utf-8
from collections import defaultdict
import re
import urllib
import urllib2
from tests.pages.block_objects import HeaderBlock, FooterBlock, PhotoGallery, ViewedTogether
from tests.static.constants import CONTACT_KEYS
from tests.utils.data_utils import convert_cyrillic_url, convert_metro_station

__author__ = 'lxz'

from wtframework.wtf.web.page import PageObject, InvalidPageError


class POIPage(PageObject, HeaderBlock, FooterBlock, PhotoGallery, ViewedTogether):
    '''
    POIPage
    WTFramework PageObject representing a page like:
    http://172.31.237.12/
    '''


    ### Page Elements Section ###
    name = lambda self: self.webdriver.find_element_by_id('poiName')
    categories = lambda self: self.webdriver.find_elements_by_xpath('//div[@id="categories"]/a')
    rating_stars = lambda self: self.webdriver.find_element_by_id('ratingStars')
    rating = lambda self: self.webdriver.find_element_by_id('rating')
    address = lambda self: self.webdriver.find_element_by_id('address')
    metro_stations = lambda self: self.webdriver.find_elements_by_xpath('//strong[@data-bind="metroName"]')
    phones = lambda self: self.webdriver.find_elements_by_xpath('//li[@data-bind="phone"]')
    emails = lambda self: self.webdriver.find_elements_by_xpath('//a[@data-bind="email"]')
    worktime = lambda self: self.webdriver.find_elements_by_xpath('//li[@data-bind="workTime"]/span[2]')
    around_the_clock = lambda self: self.webdriver.find_element_by_id('aroundTheClock')
    amenities = lambda self: self.webdriver.find_elements_by_xpath('//a[@data-bind="amenity"]')
    cuisines = lambda self: self.webdriver.find_elements_by_xpath('//a[@data-bind="cuisine"]')
    description = lambda self: self.webdriver.find_element_by_id('poiDescription')
    intro = lambda self: self.webdriver.find_element_by_id('intro')
    # image = lambda self: self.webdriver.find_element_by_xpath("//img[@data-bind=\"galleryImage\"]")
    payments = lambda self: self.webdriver.find_elements_by_xpath('//span[@data-bind="paymentName"]')
    contact_phones = lambda self: self.webdriver.find_elements_by_xpath('//li[@data-bind="phone"]')
    contact_emails = lambda self: self.webdriver.find_elements_by_xpath('//a[@data-bind="email"]')
    contact_sites = lambda self: self.webdriver.find_elements_by_xpath('//a[@data-bind="site-link"]')
    contact_social_links = lambda self: self.webdriver.find_elements_by_xpath('//a[@data-bind="social-link"]')
    average_price = lambda self: self.webdriver.find_element_by_xpath('//span[@data-bind="averagePrice"]')
    business_lunch = lambda self: self.webdriver.find_element_by_xpath('//li[@data-bind="businessLunchPrice"]')

    yandex_map = lambda self: self.webdriver.find_element_by_xpath('//section[@class="location"]/div[@class="map"]')
    checkin_time = lambda self: self.webdriver.find_element_by_xpath('//li[@data-bind="checkinTime"]')
    checkout_time = lambda self: self.webdriver.find_element_by_xpath('//li[@data-bind="checkoutTime"]')
    hotel_stars = lambda self: self.webdriver.find_element_by_id('hotelStars')
    ### End Page Elements Section ###

    def _validate_page(self, webdriver):
        if not re.search('Localway', webdriver.title):
            raise InvalidPageError("This page did not pass POIPage page validation.")

    def get_contacts_dict(self):
        d = defaultdict(list)
        [d[CONTACT_KEYS.PHONE].append(x.text) for x in self.contact_phones()]
        [d[CONTACT_KEYS.EMAIL].append(x.text) for x in self.contact_emails()]
        [d[CONTACT_KEYS.SITE].append(x.text) for x in self.contact_sites()]
        for x in self.contact_social_links():
            if CONTACT_KEYS.TWITTER in x.get_attribute('class'): d[CONTACT_KEYS.TWITTER].append(
                x.get_attribute('href'))
            if CONTACT_KEYS.VK in x.get_attribute('class'): d[CONTACT_KEYS.VK].append(
                x.get_attribute('href'))
            if CONTACT_KEYS.FACEBOOK in x.get_attribute('class'): d[CONTACT_KEYS.FACEBOOK].append(
                convert_cyrillic_url(x.get_attribute('href')))
        return d

    get_cuisines = lambda self: sorted([x.text for x in self.cuisines()])
    get_payments = lambda self: sorted([x.get_attribute('class') for x in self.payments()])
    get_metro_stations = lambda self: sorted([convert_metro_station(x.text) for x in self.metro_stations()])
    get_amenities = lambda self: sorted([x.text for x in self.amenities()])
    get_categories = lambda self: sorted([x.text for x in self.categories()])

    def get_worktime(self):
        if self.around_the_clock().is_displayed():
            return self.around_the_clock().text
        else:
            return sorted([x.text for x in self.worktime()])