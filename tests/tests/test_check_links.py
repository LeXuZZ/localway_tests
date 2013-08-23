# coding=utf-8
import itertools
from random import choice
from selenium.webdriver.common.keys import Keys
from tests.pages import ResultsListPage, HomePage
from tests.pages.leisure_section_page import LeisureSectionPage
from tests.pages.poi_page import POIPage
from tests.static.constants import SECTION_LINKS_SUFFIX, URL_PREFIXES
from tests.utils.data_utils import handle_contact_url, convert_cyrillic_url, check_oops_tooltip_position, check_dropdown_menu_for_city, check_dropdown_menu_for_language, get_digits_from_string
from tests.utils.json_utils import SectionAPI
from wtframework.wtf.web.page import PageFactory
from wtframework.wtf.config import ConfigReader
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER

__author__ = 'lxz'


class CheckLinksTest(WTFBaseTest):
    maxDiff = None

    def set_up(self):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(ConfigReader('site_credentials').get("default_url"))
        return webdriver

    def set_up_with_suffix(self, suffix):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(ConfigReader('site_credentials').get("default_url") + suffix)
        return webdriver

    def test_contact_links(self):
        webdriver = self.set_up()
        webdriver.get(ConfigReader('site_credentials').get(
            "default_url") + URL_PREFIXES.POI_ID_PREFIX + '162720af0000000000000000')
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        contact_sites = poi_page.contact_sites()
        contact_social_links = poi_page.contact_social_links()
        for contact_list in list(itertools.chain([contact_sites, contact_social_links])):
            for contact in contact_list:
                contact_url = contact.get_attribute('href')
                contact.click()
                webdriver.implicitly_wait(20)
                self.assertGreater(len(webdriver.window_handles), 1, 'link opened in the same window')
                webdriver.switch_to_window(webdriver.window_handles[-1])
                self.assertEqual(handle_contact_url(contact_url), handle_contact_url(webdriver.current_url))
                webdriver.close()
                webdriver.switch_to_window(webdriver.window_handles[-1])

    def test_contact_links_tags(self):
        webdriver = self.set_up()
        webdriver.get(ConfigReader('site_credentials').get(
            "default_url") + URL_PREFIXES.POI_ID_PREFIX + '162720af0000000000000000')
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        contact_phones = poi_page.contact_phones()
        contact_emails = poi_page.contact_emails()
        contact_sites = poi_page.contact_sites()
        contact_social_links = poi_page.contact_social_links()
        for contact_list in list(itertools.chain([contact_phones, contact_emails])):
            for contact in contact_list:
                self.assertNotEqual(contact.get_attribute('target'), '_blank')
        for contact_list in list(itertools.chain([contact_sites, contact_social_links])):
            for contact in contact_list:
                self.assertEqual(contact.get_attribute('target'), '_blank')

    def test_category_links(self):
        webdriver = self.set_up()
        webdriver.get(ConfigReader('site_credentials').get(
            "default_url") + URL_PREFIXES.POI_ID_PREFIX + '175481af0000000000000000')
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        categories = poi_page.categories()
        chosen_category = choice(categories)
        chosen_category_text = chosen_category.text
        chosen_category.click()
        webdriver.implicitly_wait(20)
        self.assertEqual(len(webdriver.window_handles), 1, 'link opened in the new tab or window')
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        categories_checked = results_list_page.categories_checked()
        self.assertEqual(len(categories_checked), 1)
        self.assertEqual(categories_checked[0].text, chosen_category_text)

    def test_amenity_links(self):
        webdriver = self.set_up()
        webdriver.get(ConfigReader('site_credentials').get(
            "default_url") + URL_PREFIXES.POI_ID_PREFIX + '175481af0000000000000000')
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        amenities = poi_page.amenities()
        chosen_amenity = choice(amenities)
        chosen_amenity_text = chosen_amenity.text
        chosen_amenity.click()
        webdriver.implicitly_wait(20)
        self.assertEqual(len(webdriver.window_handles), 1, 'link opened in the new tab or window')
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        amenities_checked = results_list_page.amenities_checked()
        self.assertEqual(len(amenities_checked), 1)
        self.assertEqual(amenities_checked[0].text, chosen_amenity_text)

    def test_cuisine_links(self):
        webdriver = self.set_up()
        webdriver.get(ConfigReader('site_credentials').get(
            "default_url") + URL_PREFIXES.POI_ID_PREFIX + '172880af0000000000000000')
        webdriver.implicitly_wait(20)
        poi_page = PageFactory.create_page(POIPage, webdriver)
        cuisines = poi_page.cuisines()
        chosen_cuisine = choice(cuisines)
        chosen_cuisine_text = chosen_cuisine.text
        chosen_cuisine.click()
        webdriver.implicitly_wait(20)
        self.assertEqual(len(webdriver.window_handles), 1, 'link opened in the new tab or window')
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)
        cuisines_checked = results_list_page.cuisines_checked()
        self.assertEqual(len(cuisines_checked), 1)
        self.assertEqual(cuisines_checked[0].text, chosen_cuisine_text)

    def test_check_home_page_header_and_footer_links(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)

        self.check_link_nonactive(home_page.header_logo_link(), webdriver, webdriver.current_url)
        self.check_link_active(home_page.header_leisure_link(), webdriver, SECTION_LINKS_SUFFIX.LEISURE)
        self.check_link_active(home_page.header_active_link(), webdriver, SECTION_LINKS_SUFFIX.ACTIVE)
        self.check_link_active(home_page.header_restaurants_link(), webdriver, SECTION_LINKS_SUFFIX.RESTAURANTS)
        self.check_link_active(home_page.header_hotels_link(), webdriver, SECTION_LINKS_SUFFIX.HOTELS)
        self.check_link_nonactive(home_page.header_events_link(), webdriver, webdriver.current_url)
        self.check_link_active(home_page.header_journeys_link(), webdriver, SECTION_LINKS_SUFFIX.JOURNEYS)
        self.check_link_nonactive(home_page.header_around_link(), webdriver, webdriver.current_url)
        self.check_link_nonactive(home_page.header_more_link(), webdriver, webdriver.current_url)

        self.assertTrue(check_dropdown_menu_for_city(home_page.header_change_city_link(), webdriver),
                        'dropdown is not visible')
        self.assertTrue(check_dropdown_menu_for_language(home_page.header_language_link(), webdriver),
                        'dropdown is not visible')
        self.assertTrue(check_oops_tooltip_position(home_page.header_register_link(), webdriver),
                        'tooltip in other place')
        self.assertTrue(check_oops_tooltip_position(home_page.header_login_link(), webdriver), 'tooltip in other place')

        self.check_link_nonactive(home_page.footer_logo_link(), webdriver, webdriver.current_url)
        self.check_link_active(home_page.footer_leisure_link(), webdriver, SECTION_LINKS_SUFFIX.LEISURE)
        self.check_link_active(home_page.footer_active_link(), webdriver, SECTION_LINKS_SUFFIX.ACTIVE)
        self.check_link_active(home_page.footer_restaurants_link(), webdriver, SECTION_LINKS_SUFFIX.RESTAURANTS)
        self.check_link_active(home_page.footer_hotels_link(), webdriver, SECTION_LINKS_SUFFIX.HOTELS)
        self.check_link_nonactive(home_page.footer_events_link(), webdriver, webdriver.current_url)
        self.check_link_active(home_page.footer_journeys_link(), webdriver, SECTION_LINKS_SUFFIX.JOURNEYS)
        self.check_link_nonactive(home_page.footer_around_link(), webdriver, webdriver.current_url)

    def test_check_results_list_page_header_and_footer_links(self):
        webdriver = self.set_up()
        home_page = PageFactory.create_page(HomePage, webdriver)
        home_page.search_for_where(u"Москва")
        home_page.search_where_input().send_keys(Keys.RETURN)
        webdriver.implicitly_wait(20)
        results_list_page = PageFactory.create_page(ResultsListPage, webdriver)

        self.check_link_active(results_list_page.header_logo_link(), webdriver, '')
        self.check_link_active(results_list_page.header_leisure_link(), webdriver, SECTION_LINKS_SUFFIX.LEISURE)
        self.check_link_active(results_list_page.header_active_link(), webdriver, SECTION_LINKS_SUFFIX.ACTIVE)
        self.check_link_active(results_list_page.header_restaurants_link(), webdriver, SECTION_LINKS_SUFFIX.RESTAURANTS)
        self.check_link_active(results_list_page.header_hotels_link(), webdriver, SECTION_LINKS_SUFFIX.HOTELS)
        self.check_link_nonactive(results_list_page.header_events_link(), webdriver, webdriver.current_url)
        self.check_link_active(results_list_page.header_journeys_link(), webdriver, SECTION_LINKS_SUFFIX.JOURNEYS)
        self.check_link_nonactive(results_list_page.header_around_link(), webdriver, webdriver.current_url)
        self.check_link_nonactive(results_list_page.header_more_link(), webdriver, webdriver.current_url)

        self.assertTrue(check_dropdown_menu_for_city(results_list_page.header_change_city_link(), webdriver),
                        'dropdown is not visible')
        self.assertTrue(check_dropdown_menu_for_language(results_list_page.header_language_link(), webdriver),
                        'dropdown is not visible')
        self.assertTrue(check_oops_tooltip_position(results_list_page.header_register_link(), webdriver),
                        'tooltip in other place')
        self.assertTrue(check_oops_tooltip_position(results_list_page.header_login_link(), webdriver),
                        'tooltip in other place')

        self.check_link_active(results_list_page.footer_logo_link(), webdriver, '')
        self.check_link_active(results_list_page.footer_leisure_link(), webdriver, SECTION_LINKS_SUFFIX.LEISURE)
        self.check_link_active(results_list_page.footer_active_link(), webdriver, SECTION_LINKS_SUFFIX.ACTIVE)
        self.check_link_active(results_list_page.footer_restaurants_link(), webdriver, SECTION_LINKS_SUFFIX.RESTAURANTS)
        self.check_link_active(results_list_page.footer_hotels_link(), webdriver, SECTION_LINKS_SUFFIX.HOTELS)
        self.check_link_nonactive(results_list_page.footer_events_link(), webdriver, webdriver.current_url)
        self.check_link_active(results_list_page.footer_journeys_link(), webdriver, SECTION_LINKS_SUFFIX.JOURNEYS)
        self.check_link_nonactive(results_list_page.footer_around_link(), webdriver, webdriver.current_url)

    def test_check_section_page_header_and_footer_links(self):
        webdriver = self.set_up_with_suffix(SECTION_LINKS_SUFFIX.LEISURE)
        leisure_section_page = PageFactory.create_page(LeisureSectionPage, webdriver)

        self.check_link_active(leisure_section_page.header_logo_link(), webdriver, '')
        self.check_link_active(leisure_section_page.header_active_link(), webdriver, SECTION_LINKS_SUFFIX.ACTIVE)
        self.check_link_active(leisure_section_page.header_leisure_link(), webdriver, SECTION_LINKS_SUFFIX.LEISURE)
        self.check_link_active(leisure_section_page.header_restaurants_link(), webdriver,
                               SECTION_LINKS_SUFFIX.RESTAURANTS)
        self.check_link_active(leisure_section_page.header_hotels_link(), webdriver, SECTION_LINKS_SUFFIX.HOTELS)
        self.check_link_nonactive(leisure_section_page.header_events_link(), webdriver, webdriver.current_url)
        self.check_link_active(leisure_section_page.header_journeys_link(), webdriver, SECTION_LINKS_SUFFIX.JOURNEYS)
        self.check_link_nonactive(leisure_section_page.header_around_link(), webdriver, webdriver.current_url)
        self.check_link_nonactive(leisure_section_page.header_more_link(), webdriver, webdriver.current_url)

        self.assertTrue(check_dropdown_menu_for_city(leisure_section_page.header_change_city_link(), webdriver),
                        'dropdown is not visible')
        self.assertTrue(check_dropdown_menu_for_language(leisure_section_page.header_language_link(), webdriver),
                        'dropdown is not visible')
        self.assertTrue(check_oops_tooltip_position(leisure_section_page.header_register_link(), webdriver),
                        'tooltip in other place')
        self.assertTrue(check_oops_tooltip_position(leisure_section_page.header_login_link(), webdriver),
                        'tooltip in other place')

        self.check_link_active(leisure_section_page.footer_logo_link(), webdriver, '')
        self.check_link_active(leisure_section_page.footer_leisure_link(), webdriver, SECTION_LINKS_SUFFIX.LEISURE)
        self.check_link_active(leisure_section_page.footer_active_link(), webdriver, SECTION_LINKS_SUFFIX.ACTIVE)
        self.check_link_active(leisure_section_page.footer_restaurants_link(), webdriver,
                               SECTION_LINKS_SUFFIX.RESTAURANTS)
        self.check_link_active(leisure_section_page.footer_hotels_link(), webdriver, SECTION_LINKS_SUFFIX.HOTELS)
        self.check_link_nonactive(leisure_section_page.footer_events_link(), webdriver, webdriver.current_url)
        self.check_link_active(leisure_section_page.footer_journeys_link(), webdriver, SECTION_LINKS_SUFFIX.JOURNEYS)
        self.check_link_nonactive(leisure_section_page.footer_around_link(), webdriver, webdriver.current_url)

    def test_check_POI_page_header_and_footer_links(self):
        webdriver = self.set_up_with_suffix(URL_PREFIXES.POI_ID_PREFIX + '172880af0000000000000000')
        poi_page = PageFactory.create_page(POIPage, webdriver)

        self.check_link_active(poi_page.header_logo_link(), webdriver, '')
        self.check_link_active(poi_page.header_leisure_link(), webdriver, SECTION_LINKS_SUFFIX.LEISURE)
        self.check_link_active(poi_page.header_active_link(), webdriver, SECTION_LINKS_SUFFIX.ACTIVE)
        self.check_link_active(poi_page.header_restaurants_link(), webdriver, SECTION_LINKS_SUFFIX.RESTAURANTS)
        self.check_link_active(poi_page.header_hotels_link(), webdriver, SECTION_LINKS_SUFFIX.HOTELS)
        self.check_link_nonactive(poi_page.header_events_link(), webdriver, webdriver.current_url)
        self.check_link_active(poi_page.header_journeys_link(), webdriver, SECTION_LINKS_SUFFIX.JOURNEYS)
        self.check_link_nonactive(poi_page.header_around_link(), webdriver, webdriver.current_url)
        self.check_link_nonactive(poi_page.header_more_link(), webdriver, webdriver.current_url)

        self.assertTrue(check_dropdown_menu_for_city(poi_page.header_change_city_link(), webdriver),
                        'dropdown is not visible')
        self.assertTrue(check_dropdown_menu_for_language(poi_page.header_language_link(), webdriver),
                        'dropdown is not visible')
        self.assertTrue(check_oops_tooltip_position(poi_page.header_register_link(), webdriver),
                        'tooltip in other place')
        self.assertTrue(check_oops_tooltip_position(poi_page.header_login_link(), webdriver), 'tooltip in other place')

        self.check_link_active(poi_page.footer_logo_link(), webdriver, '')
        self.check_link_active(poi_page.footer_leisure_link(), webdriver, SECTION_LINKS_SUFFIX.LEISURE)
        self.check_link_active(poi_page.footer_active_link(), webdriver, SECTION_LINKS_SUFFIX.ACTIVE)
        self.check_link_active(poi_page.footer_restaurants_link(), webdriver, SECTION_LINKS_SUFFIX.RESTAURANTS)
        self.check_link_active(poi_page.footer_hotels_link(), webdriver, SECTION_LINKS_SUFFIX.HOTELS)
        self.check_link_nonactive(poi_page.footer_events_link(), webdriver, webdriver.current_url)
        self.check_link_active(poi_page.footer_journeys_link(), webdriver, SECTION_LINKS_SUFFIX.JOURNEYS)
        self.check_link_nonactive(poi_page.footer_around_link(), webdriver, webdriver.current_url)

    def test_check_links_on_leisure_section_page(self):
        webdriver = self.set_up_with_suffix(SECTION_LINKS_SUFFIX.LEISURE)
        for element_number in range(len(webdriver.find_elements_by_xpath(
                '/html/body/div/section/section[2]/section/div/section/article/ul/li/a')))[1:]:
            element = webdriver.find_element_by_xpath(
                '(/html/body/div/section/section[2]/section/div/section/article/ul/li/a)[' + str(element_number) + ']')
            expected_results_count = webdriver.find_element_by_xpath(
                '(/html/body/div/section/section[2]/section/div/section/article/ul/li/span)[' + str(
                    element_number) + ']').text
            self.check_link_active(element, webdriver, 'ng/#/result?categoryName=' + element.text)
            self.assertEqual(expected_results_count, webdriver.find_element_by_xpath(
                '/html/body/div/section/section[2]/section/section/header/div/h6/span').text)

    def test_check_all_sections(self):
        webdriver = self.set_up_with_suffix(SECTION_LINKS_SUFFIX.LEISURE)
        found_count = SectionAPI().get_sections()
        for meta_section in found_count:
            print '' + meta_section['name']
            webdriver.find_element_by_xpath(
                "//span[@class=\"ng-binding\" and text()=\"" + meta_section['name'] + "\"]").click()
            for section in meta_section['sections']:
                print '     ' + section['name']
                for category in section['categories']:
                    print '         ' + category['name']
                    link_xpath = "//*[contains(@class,\'ng-scope ng-binding\') and contains(text(),\'" + category[
                            'name'] + "\')]"
                    element = webdriver.find_element_by_xpath(link_xpath)
                    element_count = get_digits_from_string(webdriver.find_element_by_xpath(link_xpath + '/following-sibling::span').text)
                    self.assertEqual(category['count'], int(element_count))
                    self.check_section_category_link(element, webdriver, 'ng/#/result?categoryName=' + category['name'],
                                                     category['count'])

    def check_section_category_link(self, webelement, webdriver, expected_url, results_count):
        if results_count == 0:
            on_section_url = webdriver.current_url
            webelement.click()
            webdriver.implicitly_wait(20)
            self.assertEqual(len(webdriver.window_handles), 1, 'link opened in the new tab or window')
            self.assertEqual(webdriver.current_url, on_section_url)
        else:
            webelement.click()
            webdriver.implicitly_wait(20)
            self.assertEqual(len(webdriver.window_handles), 1, 'link opened in the new tab or window')
            self.assertEqual(convert_cyrillic_url(webdriver.current_url),
                             ConfigReader('site_credentials').get("default_url") + expected_url)
            self.assertEqual(str(results_count), webdriver.find_element_by_xpath(
                '/html/body/div/section/section[2]/section/section/header/div[1]/h6/span').text)
            webdriver.back()


    def check_link_active(self, webelement, webdriver, expected_url):
        webelement.click()
        webdriver.implicitly_wait(20)
        self.assertEqual(len(webdriver.window_handles), 1, 'link opened in the new tab or window')
        self.assertEqual(convert_cyrillic_url(webdriver.current_url),
                         ConfigReader('site_credentials').get("default_url") + expected_url)
        webdriver.back()

    def check_link_nonactive(self, webelement, webdriver, expected_url):
        webelement.click()
        webdriver.implicitly_wait(20)
        self.assertEqual(len(webdriver.window_handles), 1, 'link opened in the new tab or window')
        self.assertEqual(webdriver.current_url, expected_url)