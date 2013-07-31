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
from tests.static.constants import POI_KEYS
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
    return re.search('[0-9]', string).group()


def delete_newlines_for_description_and_intro(string):
    restring = re.sub("^\s+|\n+|\r+|\s+$", ' ', string)
    restring_second = re.sub("\s+", ' ', restring)
    return delete_whitespace_edges(restring_second)


def delete_whitespace_edges(string):
    return re.sub("^\s+|\s+$", '', string)


def create_address_from_poi(poi):
    address = ''
    if POI_KEYS.CITY in poi:
        address += MongoDB().convert_city_id_to_name(poi[POI_KEYS.CITY]).encode('utf-8')
    if POI_KEYS.STREET in poi:
        address += ', ' + 'ул. ' + poi[POI_KEYS.STREET].encode('utf-8')
    if POI_KEYS.HOUSE in poi:
        address += ', ' + 'д. ' + poi[POI_KEYS.HOUSE].encode('utf-8')
    if POI_KEYS.BUILDING in poi:
        address += ', ' + poi[POI_KEYS.BUILDING].encode('utf-8')
    return unicode(address, 'utf-8')


def create_dict_for_contacts(poi):
    d = defaultdict(list)
    for contact in poi[POI_KEYS.CONTACTS]:
        contact_key = MongoDB().convert_contact_type_id_to_name(contact[POI_KEYS.CONTACT_TYPE]).encode('utf-8')
        # d[contact_key].append(delete_whitespace_edges(contact[POI_KEYS.CONTACT]) if ('http://' in contact[POI_KEYS.CONTACT]) or (contact_key == 'Телефон' or contact_key == 'EMail') else 'http://' + delete_whitespace_edges(contact[POI_KEYS.CONTACT]))
        if ('http://' in contact[POI_KEYS.CONTACT]) or (contact_key == 'Телефон' or contact_key == 'EMail'):
            d[contact_key].append(delete_whitespace_edges(contact[POI_KEYS.CONTACT]))
        elif ('https://' in contact[POI_KEYS.CONTACT]) or (contact_key == 'Телефон' or contact_key == 'EMail'):
            d[contact_key].append(delete_whitespace_edges(contact[POI_KEYS.CONTACT]))
        else:
            d[contact_key].append('http://' + delete_whitespace_edges(contact[POI_KEYS.CONTACT]))
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


def convert_average_price_from_poi(poi):
    if not poi[POI_KEYS.AVERAGE_PRICE]:
        return u''
    else:
        return poi[POI_KEYS.AVERAGE_PRICE][0] + ' - ' + poi[POI_KEYS.AVERAGE_PRICE][1]


def convert_business_lunch_from_poi(poi):
    d = ''
    if not poi[POI_KEYS.BUSINESS_LUNCH_PRICE]:
        return u''
    else:
        if poi[POI_KEYS.BUSINESS_LUNCH_PRICE][0] in '':
            d += (u'до ' + poi[POI_KEYS.BUSINESS_LUNCH_PRICE])
        if poi[POI_KEYS.BUSINESS_LUNCH_PRICE][1] in '':
            d += (u'от ' + poi[POI_KEYS.BUSINESS_LUNCH_PRICE][0])
        if poi[POI_KEYS.BUSINESS_LUNCH_PRICE][0] and poi[POI_KEYS.BUSINESS_LUNCH_PRICE][1] not in '':
            d += (poi[POI_KEYS.BUSINESS_LUNCH_PRICE][0] + ' - ' + poi[POI_KEYS.BUSINESS_LUNCH_PRICE][1])
    return d