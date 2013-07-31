# coding=utf-8
from collections import defaultdict
import re
import urllib
import urllib2
from tests.static.constants import CONTACT_KEYS

__author__ = 'lxz'

from wtframework.wtf.web.page import PageObject, InvalidPageError


class POIPage(PageObject):
    '''
    POIPage
    WTFramework PageObject representing a page like:
    http://172.31.237.12/
    '''


    ### Page Elements Section ###
    name = lambda self: self.webdriver.find_element_by_xpath("//span[@data-bind=\"poiName\"]")
    categories = lambda self: self.webdriver.find_elements_by_xpath("//div[@data-bind=\"categories\"]/a")
    rating_stars = lambda self: self.webdriver.find_element_by_xpath(
        "/html/body/section/article/section[2]/section/header/div/span")
    rating = lambda self: self.webdriver.find_element_by_xpath("//span[@data-bind=\"rating\"]")
    address = lambda self: self.webdriver.find_element_by_xpath("//section[@class=\"poi-info\"]/div[@class=\"address\"]")
    metro_stations = lambda self: self.webdriver.find_elements_by_xpath(
        "//div[@data-bind=\"metroStations\"]//*[@data-bind=\"name\"]")
    phones = lambda self: self.webdriver.find_elements_by_xpath("//ul[@data-bind=\"phones\"]")
    emails = lambda self: self.webdriver.find_elements_by_xpath("//a[@data-bind=\"email\"]")
    worktime = lambda self: self.webdriver.find_elements_by_xpath("//span[@data-bind=\"worktime\"]")
    around_the_clock = lambda self: self.webdriver.find_element_by_xpath("//div[@data-bind=\"aroundTheClock\"]")
    amenities = lambda self: self.webdriver.find_elements_by_xpath("//div[@data-bind=\"amenities\"]/div/a")
    cuisines = lambda self: self.webdriver.find_elements_by_xpath("//div[@data-bind=\"cuisines\"]/div/a")
    description = lambda self: self.webdriver.find_element_by_xpath("//p[@data-bind=\"description\"]")
    intro = lambda self: self.webdriver.find_element_by_xpath("//h5[@data-bind=\"intro\"]")
    image = lambda self: self.webdriver.find_element_by_xpath("//img[@data-bind=\"galleryImage\"]")
    payments = lambda self: self.webdriver.find_elements_by_xpath(
        "//ul[@data-bind=\"payments\"]/li/span[@data-bind=\"link\"]")
    contact_phones = lambda self: self.webdriver.find_elements_by_xpath(
        "//div[@data-bind=\"contacts\"]/ul[@data-bind=\"phones\"]/li")
    contact_emails = lambda self: self.webdriver.find_elements_by_xpath(
        "//div[@data-bind=\"contacts\"]/ul[@data-bind=\"links\"]//*[@data-bind=\"email\"]")
    contact_sites = lambda self: self.webdriver.find_elements_by_xpath(
        "//div[@data-bind=\"contacts\"]/ul[@data-bind=\"links\"]//*[@data-bind=\"link\"]")
    contact_social_links = lambda self: self.webdriver.find_elements_by_xpath(
        "//div[@data-bind=\"contacts\"]/ul[@data-bind=\"social-links\"]/li/a")
    average_price = lambda self: self.webdriver.find_element_by_xpath("//span[@data-bind=\"averagePrice\"]")
    business_lunch = lambda self: self.webdriver.find_element_by_xpath("//span[@data-bind=\"businessLunchPrice\"]")

    yandex_map = lambda self: self.webdriver.find_element_by_xpath(
        "//section[@class=\"location\"]/div[@class=\"map\"]")
    checkin_time = lambda self: self.webdriver.find_element_by_xpath("//span[@data-bind=\"checkinTime\"]")
    checkout_time = lambda self: self.webdriver.find_element_by_xpath("//span[@data-bind=\"checkoutTime\"]")
    hotel_stars = lambda self: self.webdriver.find_element_by_xpath(
        "/html/body/section/article/section[2]/section/header/h2/span[2]")
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
                urllib2.unquote(x.get_attribute('href').encode('ASCII')).decode('utf8'))
        return d

    get_cuisines = lambda self: sorted([x.text for x in self.cuisines()])
    get_payments = lambda self: sorted([x.get_attribute('class') for x in self.payments()])
    get_metro_stations = lambda self: sorted([x.text for x in self.metro_stations()])
    get_amenities = lambda self: sorted([x.text for x in self.amenities()])
    get_categories = lambda self: sorted([x.text for x in self.categories()])

    def get_worktime(self):
        if self.around_the_clock().is_displayed():
            return self.around_the_clock().text
        else:
            return sorted([x.text for x in self.worktime()])