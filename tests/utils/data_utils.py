# coding=utf-8
##########################################################################
#This file is part of WTFramework. 
#
#    WTFramework is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WTFramework is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WTFramework.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################
"""
The purpose of this module is to provide functions for generating data that 
can be used in tests.
"""
from collections import defaultdict
from datetime import datetime
import re
import time
import random
import string
import urllib2
from bson import ObjectId
import itertools
from pymongo import MongoClient
from selenium.webdriver import ActionChains
from tests.utils.weight_util import distance
from wtframework.wtf.config import ConfigReader
from tests.static.constants import POI_KEYS
from tests.utils.json_utils import PortalAPI
from tests.utils.mongo_utils import MongoDB


def generate_timestamped_string(subject, number_of_random_chars=4):
    """
    Generate time-stamped string. Format as follows...
    2013-01-31_14:12:23_SubjectString_a3Zg
    @param subject: String to use as subject.
    @type subject: str
    """
    random_str = generate_random_string(number_of_random_chars)
    timestamp = generate_timestamp()
    return "{timestamp}_{subject}_{random_str}".format(timestamp=timestamp,
                                                       subject=subject,
                                                       random_str=random_str)


def generate_timestamp(date_format="%Y-%m-%d_%H.%M.%S"):
    """
    Returns timestamped string. '2012-03-15_14:42:23
    @param format: A date/time format string.  If not specified, the default will be used.
    """
    return datetime.now().strftime(date_format)


def generate_random_string(number_of_random_chars=8, character_set=string.ascii_letters):
    """
    Generate a series of random chracters.
    @param number_of_random_chars: Number of characters long
    @param character_set: Specify a character set.  Default is ASCII
    """
    return ''.join(random.choice(character_set) \
                   for _ in range(number_of_random_chars))


def convert_ms_to_HM(time_in_ms):
    return time.strftime('%H:%M', time.gmtime(time_in_ms / 1000))


def crop_first_zero_if_exist(time):
    time = time[1:] if time[0] == '0' else time
    return time


def get_digits_from_string(string):
    return re.search('[0-9]+', string).group()


def delete_newlines_for_description_and_intro(string):
    restring = re.sub("^\s+|\n+|\r+|\s+$", ' ', string)
    restring_second = re.sub("\s+", ' ', restring)
    return delete_whitespace_edges(restring_second)


def delete_whitespace_edges(string):
    return re.sub("^\s+|\s+$", '', string)


def create_address_from_poi(poi):
    address = ''
    if POI_KEYS.CITY in poi and poi[POI_KEYS.CITY] is not u'':
        address += MongoDB().convert_city_id_to_name(poi[POI_KEYS.CITY]).encode('utf-8')
    if POI_KEYS.STREET in poi and poi[POI_KEYS.STREET] is not u'':
        address += ' ' + 'ул. ' + delete_whitespace_edges(poi[POI_KEYS.STREET].encode('utf-8'))
    if POI_KEYS.HOUSE in poi and poi[POI_KEYS.HOUSE] is not u'':
        address += ' ' + 'д. ' + delete_whitespace_edges(poi[POI_KEYS.HOUSE].encode('utf-8'))
    if POI_KEYS.BUILDING in poi and poi[POI_KEYS.BUILDING] is not u'':
        address += ' ' + delete_whitespace_edges(poi[POI_KEYS.BUILDING].encode('utf-8'))
    return unicode(address, 'utf-8')


def create_dict_for_contacts(poi):
    d = defaultdict(list)
    for contact in poi[POI_KEYS.CONTACTS]:
        contact_key = MongoDB().convert_contact_type_id_to_name(contact[POI_KEYS.CONTACT_TYPE]).encode('utf-8')
        # d[contact_key].append(delete_whitespace_edges(contact[POI_KEYS.CONTACT]) if ('http://' in contact[POI_KEYS.CONTACT]) or (contact_key == 'Телефон' or contact_key == 'EMail') else 'http://' + delete_whitespace_edges(contact[POI_KEYS.CONTACT]))
        if ('http://' in contact[POI_KEYS.CONTACT]) or (contact_key == 'Телефон' or contact_key == 'EMail'):
            d[contact_key].append(convert_cyrillic_url(delete_whitespace_edges(contact[POI_KEYS.CONTACT])))
        elif ('https://' in contact[POI_KEYS.CONTACT]) or (contact_key == 'Телефон' or contact_key == 'EMail'):
            d[contact_key].append(convert_cyrillic_url(delete_whitespace_edges(contact[POI_KEYS.CONTACT])))
        else:
            d[contact_key].append('http://' + convert_cyrillic_url(delete_whitespace_edges(contact[POI_KEYS.CONTACT])))
    return d


def convert_working_time_from_poi(poi):
    d = []
    if POI_KEYS.AROUND_THE_CLOCK in poi.keys():
        if poi[POI_KEYS.AROUND_THE_CLOCK]:
            return u'Круглосуточно'
    for time in poi[POI_KEYS.WORK_TIME]:
        time_from = crop_first_zero_if_exist(convert_ms_to_HM(time['timeFrom']))
        time_to = crop_first_zero_if_exist(convert_ms_to_HM(time['timeTo']))
        d.append((time_from + ' - ' + time_to).decode('utf-8'))
    return sorted(d)


def convert_metro_station(metro_name):
    return re.sub(u'м. ', '', metro_name)


def convert_prices_from_poi_json(poi):
    if poi['free']:
        return poi['name'] + u': ' + u'бесплатно'
    if 'from' in poi and 'to' in poi:
        return poi['name'] + u': ' + str(poi['from']) + ' - ' + str(poi['to']) + u' р.'
    if 'from' in poi:
        return poi['name'] + u': ' + u'от ' + str(poi['from']) + u' р.'
    if 'to' in poi:
        return poi['name'] + u': ' + u'до ' + str(poi['to']) + u' р.'


def delete_last_slash_if_exist(string):
    return re.sub('/$', '', string)


def conver_https_to_http(string):
    return re.sub('https:', 'http:', string)


def handle_contact_url(string):
    return delete_last_slash_if_exist(conver_https_to_http(string))


def convert_cyrillic_url(url):
    return urllib2.unquote(url.encode('ASCII')).decode('utf8')


def get_center_of_webelement(webelement):
    return [webelement.size['width'] / 2, webelement.size['height'] / 2]


def get_top_center_of_webelement(webelement):
    return [webelement.size['width'] / 2, 0]


def get_bottom_center_of_webelement(webelement):
    return [webelement.size['width'] / 2, webelement.size['height']]


def get_global_position(webelement, point):
    return {'x': webelement.location['x'] + point[0], 'y': webelement.location['y'] + point[1]}


def check_oops_tooltip_position(webelement, webdriver):
    # ActionChains(webdriver).move_to_element(webelement).click()
    webelement.click()
    tooltip = webdriver.find_element_by_xpath('//div[contains(@id,"ui-tooltip")]')
    webelement_pos = get_global_position(webelement, get_bottom_center_of_webelement(webelement))
    tooltip_pos = get_global_position(tooltip, get_top_center_of_webelement(tooltip))
    # if abs(webelement_pos['x'] - tooltip_pos['x']) == 0 and abs(webelement_pos['y'] - tooltip_pos['y']) == 9:
    if abs(webelement_pos['y'] - tooltip_pos['y']) == 9:
        return True
    else:
        return False


def check_dropdown_menu(webelement, webdriver, element_counter):
    # ActionChains(webdriver).move_to_element(webelement).click_and_hold(webelement)
    ActionChains(webdriver).move_to_element(webelement).click().perform()
    webelement.click()
    webdriver.implicitly_wait(5)
    dropdown = webdriver.find_element_by_xpath('//header/section[2]/ul/li[' + str(element_counter) + ']/div/ul')
    if dropdown.size['height'] > 0:
        return True
    else:
        return False


def check_dropdown_menu_for_city(webelement, webdriver):
    return check_dropdown_menu(webelement, webdriver, 2)


def check_dropdown_menu_for_language(webelement, webdriver):
    return check_dropdown_menu(webelement, webdriver, 6)


def get_image_id_from_src(src):
    return re.search('/(\d+)_', src).group(1)


def get_time_from_check_info(info):
    return re.search('\d{2}:\d{2}', info).group(0)


def get_name_from_auto_suggestion(info):
    return re.search('(.*)\n', info).group(1)


def create_stub_data_for_autosuggestion():
    suggestion = defaultdict(list)
    suggestion['categories'].append(u'Веганский ресторан')
    suggestion['categories'].append(u'Вегатарианский ресторан')
    suggestion['categories'].append(u'Ресторан')
    suggestion['categories'].append(u'Ресторанный дворик')
    suggestion['categories'].append(u'Рыбный ресторан')

    suggestion['pois'].append(
        dict(address=u'Певческий пер, 6', name=u'Экспедиция. Ресторан', rating=u'5', bolded_name=u'Рест'))
    suggestion['pois'].append(
        dict(address=u'Ленинградское шоссе, 16а ст4', name=u'Чемпион. Ресторан и бар', rating=u'4',
             bolded_name=u'Рест'))
    suggestion['pois'].append(
        dict(address=u'Мира проспект, 91 корпус 3', name=u'Океан. Ресторан', rating=u'3', bolded_name=u'Рест'))
    return suggestion


def query_format(text, query):
    return re.sub('QUERY_TEXT', str(text), query)


def round_distance(distance):
    if distance < 950:
        result = str(int(round(distance / 10) * 10))
        if result > 0:
            result += ' м'
    else:
        result = str(round(distance / 100) / 10)
        if result > 0:
            result += ' км'
    return result


def get_name_without_digits_in_brackets(text):
    return re.search('(.+)\s\(', text).group(1)


def timer(f):
    def tmp(*args, **kwargs):
        t = time.time()
        res = f(*args, **kwargs)
        print "Время выполнения %s: %f" % (f.__name__, time.time() - t)
        return res

    return tmp


@timer
def get_recommendations_for_poi(poi_id):
    all_needed_pois_list = []
    #category_sections = {str(x['_id']): x['name'] for x in [x for x in MongoClient(ConfigReader('db').get("mongodb_auth"))['localway'].sections.find({'categories': ObjectId(str([x for x in MongoClient(ConfigReader('db').get("mongodb_auth"))['localway'].pois.find_one({"_id": ObjectId('225946af0000000000000000')})['categoriesWithPriority'] if 'priority' in x and x['priority'] == 1][0]['categoryId']))})]}
    poi = MongoDB().get_poi_by_id(poi_id)
    main_category_id = str(
        [x for x in poi['categoriesWithPriority'] if 'priority' in x and x['priority'] == 1][0]['categoryId'])
    category_sections = {str(x['_id']): x['name'] for x in MongoDB().get_sections_by_main_category_id(main_category_id)}
    config = PortalAPI.get_config_for_around_poi()
    all_c_recommendations = {}
    all_s_recommendations = {}
    excluded_recommendations = {}
    is_main_category_in_reccomendations = False
    for recommendation in config['config']:
        if 'c_ids' in recommendation:
            if main_category_id in recommendation['c_ids']:
                is_main_category_in_reccomendations = True
                if 'categories' in recommendation:
                    all_c_recommendations.update(
                        {x: MongoDB().convert_category_id_to_name(x) for x in recommendation['categories']})
                if 'sections' in recommendation:
                    all_s_recommendations.update(
                        {x: MongoDB().convert_section_id_to_name(x) for x in recommendation['sections']})
                if 'category_excludes' in recommendation:
                    excluded_recommendations.update(
                        {x: MongoDB().convert_category_id_to_name(x) for x in recommendation['category_excludes']})
    if not is_main_category_in_reccomendations:
        for recommendation in config['config']:
            if 's_ids' in recommendation:
                for section_id in category_sections.keys():
                    if section_id in recommendation['s_ids']:
                        if 'categories' in recommendation:
                            all_c_recommendations.update(
                                {x: MongoDB().convert_category_id_to_name(x) for x in recommendation['categories']})
                        if 'sections' in recommendation:
                            all_s_recommendations.update(
                                {x: MongoDB().convert_section_id_to_name(x) for x in recommendation['sections']})
                        if 'category_excludes' in recommendation:
                            excluded_recommendations.update(
                                {x: MongoDB().convert_category_id_to_name(x) for x in recommendation['category_excludes']})
        recommended_pois_by_section_a = [list(itertools.chain.from_iterable([MongoDB().get_pois_with_needed_main_category_and_coords(y) for y in MongoDB().get_section_categories(x)])) for x in all_s_recommendations.keys()]
        recommended_pois_by_section = [[y for y in x if 'priority' in y['categoriesWithPriority'][0] and y['categoriesWithPriority'][0]['priority'] == 1 and str(y['categoriesWithPriority'][0]['categoryId']) not in excluded_recommendations.keys()] for x in recommended_pois_by_section_a]
        sorted_by_nearest_recommended_pois_list_by_sections = [sorted(x, key=lambda recommended_poi: (distance(poi['lat'], poi['lon'], recommended_poi['lat'], recommended_poi['lon']), recommended_poi['name'])) for x in recommended_pois_by_section]
        sorted_by_nearest_recommended_pois_list_by_sections_with_rating = [sorted(x, key=lambda recommended_poi: (recommended_poi['rating']), reverse=True)[:2] for x in sorted_by_nearest_recommended_pois_list_by_sections]
        for i, l in enumerate(sorted_by_nearest_recommended_pois_list_by_sections):
            all_needed_pois_list.append((sorted_by_nearest_recommended_pois_list_by_sections_with_rating[i] + [x for x in l if x not in sorted_by_nearest_recommended_pois_list_by_sections_with_rating[i]])[:100])

    recommended_pois_by_category_a = [MongoDB().get_pois_with_existing_category_and_coords(x) for x in all_c_recommendations.keys()]
    recommended_pois_by_category = [[y for y in x if 'priority' in y['categoriesWithPriority'][0] and y['categoriesWithPriority'][0]['priority'] == 1 and str(y['categoriesWithPriority'][0]['categoryId']) not in excluded_recommendations.keys()] for x in recommended_pois_by_category_a]
    sorted_by_nearest_recommended_pois_list_by_categories = [sorted(x, key=lambda recommended_poi: (distance(poi['lat'], poi['lon'], recommended_poi['lat'], recommended_poi['lon']), recommended_poi['name'])) for x in recommended_pois_by_category]
    sorted_by_nearest_recommended_pois_list_by_categories_with_rating = [sorted(x, key=lambda recommended_poi: (recommended_poi['rating']), reverse=True)[:2] for x in sorted_by_nearest_recommended_pois_list_by_categories]


    for i, l in enumerate(sorted_by_nearest_recommended_pois_list_by_categories):
        all_needed_pois_list.append((sorted_by_nearest_recommended_pois_list_by_categories_with_rating[i] + [x for x in l if x not in sorted_by_nearest_recommended_pois_list_by_categories_with_rating[i]])[:100])
    #for y in all_needed_pois_list:
    #    for i in y:
    #        print i['name'] + ' ' + str(distance(poi['lat'], poi['lon'], i['lat'], i['lon'])) + ' rating: ' + str(i['rating'])
    #    print 'SPLITTED'
    return all_needed_pois_list


