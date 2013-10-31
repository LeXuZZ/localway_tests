from collections import defaultdict
from random import choice
from selenium.webdriver import ActionChains
from tests.utils.data_utils import get_name_from_auto_suggestion, get_digits_from_string

__author__ = 'lxz'


class SearchBlock():
    def __init__(self):
        pass

    search_what_input = lambda self: self.webdriver.find_element_by_id("input-what")
    search_where_input = lambda self: self.webdriver.find_element_by_id("input-where")
    search_button = lambda self: self.webdriver.find_element_by_id("searchButton")
    search_locate_me_button = lambda self: self.webdriver.find_element_by_id('searchLocateMeButton')


class HeaderBlock():
    def __init__(self):
        pass

    header_leisure_link = lambda self: self.webdriver.find_element_by_xpath('//header/section/nav/a[1]')
    header_active_link = lambda self: self.webdriver.find_element_by_xpath('//header/section/nav/a[2]')
    header_restaurants_link = lambda self: self.webdriver.find_element_by_xpath('//header/section/nav/a[3]')
    header_hotels_link = lambda self: self.webdriver.find_element_by_xpath('//header/section/nav/a[4]')
    header_events_link = lambda self: self.webdriver.find_element_by_xpath('//header/section/nav/a[5]')
    header_journeys_link = lambda self: self.webdriver.find_element_by_xpath('//header/section/nav/a[6]')
    header_around_link = lambda self: self.webdriver.find_element_by_xpath('//header/section/nav/a[7]')
    header_more_link = lambda self: self.webdriver.find_element_by_xpath('//header/section/nav/a[8]')

    header_logo_link = lambda self: self.webdriver.find_element_by_xpath('//header/section[2]/ul/li[1]/a')
    header_change_city_link = lambda self: self.webdriver.find_element_by_xpath('//header/section[2]/ul/li[2]/div')
    header_register_link = lambda self: self.webdriver.find_element_by_xpath('//header/section[2]/ul/li[4]')
    header_login_link = lambda self: self.webdriver.find_element_by_xpath('//header/section[2]/ul/li[5]')
    header_language_link = lambda self: self.webdriver.find_element_by_xpath('//header/section[2]/ul/li[6]/div')


class FooterBlock():
    def __init__(self):
        pass

    footer_leisure_link = lambda self: self.webdriver.find_element_by_xpath('//footer/section/nav/a[1]')
    footer_active_link = lambda self: self.webdriver.find_element_by_xpath('//footer/section/nav/a[2]')
    footer_restaurants_link = lambda self: self.webdriver.find_element_by_xpath('//footer/section/nav/a[3]')
    footer_hotels_link = lambda self: self.webdriver.find_element_by_xpath('//footer/section/nav/a[4]')
    footer_events_link = lambda self: self.webdriver.find_element_by_xpath('//footer/section/nav/a[5]')
    footer_journeys_link = lambda self: self.webdriver.find_element_by_xpath('//footer/section/nav/a[6]')
    footer_around_link = lambda self: self.webdriver.find_element_by_xpath('//footer/section/nav/a[7]')

    footer_logo_link = lambda self: self.webdriver.find_element_by_xpath('//footer/section[2]/a')


class PhotoGallery():
    def __init__(self):
        pass

    gallery_main = lambda self: self.webdriver.find_element_by_xpath('//lw-gallery/div')
    gallery_previous = lambda self: self.webdriver.find_element_by_xpath('//a[@class="slide-prev"]')
    gallery_next = lambda self: self.webdriver.find_element_by_xpath('//a[@class="slide-next"]')
    move_to_thumbnails = lambda self: ActionChains(self.webdriver).move_to_element(self.webdriver.find_element_by_xpath(
        '//div[@class="thumbnails"]')).perform()
    thumbnails_previous = lambda self: self.webdriver.find_element_by_xpath('//div[@class="thumbnails"]/a[1])')
    thumbnails_next = lambda self: self.webdriver.find_element_by_xpath('//div[@class="thumbnails"]/a[2]')
    thumbnails_list = lambda self: self.webdriver.find_elements_by_xpath('//div[@class="thumbs-list"]/a')
    get_images = lambda self: self.webdriver.find_elements_by_xpath('//div[@class="img-container"]/img')
    get_circles = lambda self: self.webdriver.find_elements_by_xpath(
        '//div[@class="see-all"]/div[@class="circles"]/span')

    get_center_image = lambda self: self.get_images()[1]


class ViewedTogether():
    def __init__(self):
        pass

    vt_blocks = lambda self: self.webdriver.find_elements_by_xpath('//aside/section[3]/section/a')

    vt_images = lambda self: self.webdriver.find_elements_by_xpath('//img[@data-bind="vt-image"]')
    vt_hotel_stars = lambda self: self.webdriver.find_elements_by_xpath('//span[@data-bind="vt-hotelStars"]')
    vt_names = lambda self: self.webdriver.find_elements_by_xpath('//p[@data-bind="vt-poiName"]')
    vt_ratings = lambda self: self.webdriver.find_elements_by_xpath('//span[@data-bind="vt-rating"]')
    vt_category = lambda self: self.webdriver.find_elements_by_xpath('//span[@data-bind="vt-category"]')
    vt_address = lambda self: self.webdriver.find_elements_by_xpath('//span[@data-bind="vt-address"]')

    vt_show_map = lambda self, number: self.webdriver.find_element_by_xpath(
        '//a[' + str(number) + ']/div/div/span[4]/span[2]/span')

    vt_modal_map = lambda self: self.webdriver.find_element_by_xpath('//lw-modal[@call-as="showPoiModal"]/div')

    def open_vt_map(self, number):
        image = self.vt_images()[number]
        link = self.vt_show_map(number + 1)
        ActionChains(self.webdriver).move_to_element(image).move_to_element(link).click().perform()

    def get_viewed_together_info(self):
        viewed_together = defaultdict(list)
        names = [x.text for x in self.vt_names()]
        hotel_stars_elements = self.vt_hotel_stars()
        hotel_stars = []
        for element in hotel_stars_elements:
            if element.is_displayed():
                hotel_stars.append(get_digits_from_string(element.get_attribute('class')))
            else:
                hotel_stars.append('')
        ratings = [get_digits_from_string(x.get_attribute('class')) for x in self.vt_ratings()]
        categories = [x.text for x in self.vt_category()]
        address = [x.text for x in self.vt_address()]
        for i in range(len(names)):
            poi_info = dict(name=names[i], hotel_stars=hotel_stars[i], rating=ratings[i],
                            categories=categories[i], address=address[i])
            viewed_together['pois'].append(poi_info)
        return viewed_together


class AroundPOI():
    def __init__(self):
        pass

    ar_blocks = lambda self: self.webdriver.find_elements_by_xpath('//aside/section[2]/section/a')

    ar_images = lambda self: self.webdriver.find_elements_by_xpath('//img[@data-bind="ar-image"]')
    ar_hotel_stars = lambda self: self.webdriver.find_elements_by_xpath('//span[@data-bind="ar-hotelStars"]')
    ar_names = lambda self: self.webdriver.find_elements_by_xpath('//p[@data-bind="ar-poiName"]')
    ar_ratings = lambda self: self.webdriver.find_elements_by_xpath('//span[@data-bind="ar-rating"]')
    ar_category = lambda self: self.webdriver.find_elements_by_xpath('//span[@data-bind="ar-category"]')
    ar_address = lambda self: self.webdriver.find_elements_by_xpath('//span[@data-bind="ar-address"]')
    ar_show_more = lambda self: self.webdriver.find_element_by_xpath('//aside/section[2]/a[@ng-show="canShowMore()"]')
    ar_collapse = lambda self: self.webdriver.find_element_by_xpath('//aside/section[2]/a[@ng-show="canCollapse()"]')

    def get_around_poi_info(self):
        around_poi = defaultdict(list)
        names = [x.text for x in self.ar_names()]
        hotel_stars_elements = self.ar_hotel_stars()
        hotel_stars = []
        for element in hotel_stars_elements:
            if element.is_displayed():
                hotel_stars.append(get_digits_from_string(element.get_attribute('class')))
            else:
                hotel_stars.append('')
        ratings = [get_digits_from_string(x.get_attribute('class')) for x in self.ar_ratings()]
        categories = [x.text for x in self.ar_category()]
        address = [x.text for x in self.ar_address()]
        for i in range(len(names)):
            poi_info = dict(name=names[i], hotel_stars=hotel_stars[i], rating=ratings[i],
                            categories=categories[i], address=address[i])
            around_poi['pois'].append(poi_info)
        return around_poi

    def click_show_more(self):
        while not self.ar_collapse().is_displayed():
            self.ar_show_more().click()


class AutoSuggestion():
    def __init__(self):
        pass

    as_addresses = lambda self: self.webdriver.find_elements_by_xpath('//span[@data-bind="as-poi-address"]')
    as_ratings = lambda self: self.webdriver.find_elements_by_xpath('//span[@data-bind="as-poi-rating"]')
    as_names = lambda self: self.webdriver.find_elements_by_xpath('//p[@data-bind="as-poi-name"]')
    as_bolded_names = lambda self: self.webdriver.find_elements_by_xpath('//p[@data-bind="as-poi-name"]/strong')
    as_categories = lambda self: self.webdriver.find_elements_by_xpath('//li[@data-bind="as-category-name"]/a')

    def get_autosuggestion(self):
        suggestion = defaultdict(list)
        categories = self.as_categories()
        addresses = [x.text for x in self.as_addresses()]
        names = [get_name_from_auto_suggestion(x.text) for x in self.as_names()]
        ratings = [get_digits_from_string(x.get_attribute('class')) for x in self.as_ratings()]
        bolded_names = [x.text for x in self.as_bolded_names()]
        for i in range(len(names)):
            poi_info = dict(address=addresses[i], name=names[i], rating=ratings[i], bolded_name=bolded_names[i])
            suggestion['pois'].append(poi_info)
        [suggestion['categories'].append(x.text) for x in categories]
        return suggestion


class ResultsListPOIBrief():
    def __init__(self):
        pass

    brief_locator = '//a[@data-bind="brief"]'
    brief_name_locator = '//h4[@data-bind="brief_name"]'
    brief_categories_locator = '//div[@data-bind="brief_categories"]'
    brief_category_locator = '//span[@data-bind="brief_category"]'
    brief_rating_locator = '//span[@data-bind="brief_rating"]'
    brief_address_locator = '//p[@data-bind="brief_address"]'
    brief_metro_stations_locator = '//p[@data-bind="brief_address"]'
    brief_metro_name_locator = '//span[@data-bind="brief_metroName"]'
    brief_distance_locator = '//span[@data-bind="brief_distanceInMeters"]'

    briefs = lambda self: self.webdriver.find_elements_by_xpath(self.brief_locator)
    brief_name = lambda self, number: self.webdriver.find_element_by_xpath(
        self.brief_locator + '[' + str(number) + ']' + self.brief_name_locator).text
    brief_address = lambda self, number: self.webdriver.find_element_by_xpath(
        self.brief_locator + '[' + str(number) + ']' + self.brief_address_locator).text
    brief_rating = lambda self, number: get_digits_from_string(self.webdriver.find_element_by_xpath(
        self.brief_locator + '[' + str(number) + ']' + self.brief_rating_locator).get_attribute('class'))
    brief_categories = lambda self, number: [x.text for x in self.webdriver.find_elements_by_xpath(
        self.brief_locator + '[' + str(number) + ']' + self.brief_category_locator)]
    brief_metro = lambda self, number: [x.text for x in self.webdriver.find_elements_by_xpath(
        self.brief_locator + '[' + str(number) + ']' + self.brief_metro_name_locator)]
    brief_distance = lambda self, number: self.webdriver.find_element_by_xpath(
        self.brief_locator + '[' + str(number) + ']' + self.brief_distance_locator).text

    def get_results(self):
        results = defaultdict(list)
        length = len(self.briefs())
        for i in range(1, length + 1):
            poi_info = dict(name=self.brief_name(i), address=self.brief_address(i), rating=self.brief_rating(i),
                            categories=self.brief_categories(i), metro=self.brief_metro(i),
                            distance=self.brief_distance(i))
            results['pois'].append(poi_info)
        return results

    def open_random_poi_page(self):
        choice(self.briefs()).click()

class LocateMe():
    def __init__(self):
        pass

    lm_input_address_locator = 'input-address'
    lm_location_enabled_locator = 'location_enabled'
    lm_location_disabled_locator = 'location_disabled'
    lm_input_address = lambda self: self.webdriver.find_element_by_id(self.lm_input_address_locator)
    lm_locate_me_button = lambda self: self.webdriver.find_element_by_id('locateMe')
    lm_location_enabled = lambda self: self.webdriver.find_element_by_id(self.lm_location_enabled_locator)
    lm_location_disabled = lambda self: self.webdriver.find_element_by_id(self.lm_location_disabled_locator)
    lm_save_button_enabled = lambda self: self.webdriver.find_element_by_id('save_button_enabled')
    lm_save_button_disabled = lambda self: self.webdriver.find_element_by_id('save_button_disabled')

    lm_map_pin = lambda self: self.webdriver.find_element_by_xpath('//ymaps[contains(@id,"id_")]/..')