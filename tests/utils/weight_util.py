# coding=utf-8
import json
import re
import math

import requests
import geopy
import geopy.distance
from decimal import Decimal

from tests.static.constants import WEIGHT, YANDEX_MAPS_API_REQUESTS
from tests.utils.mongo_utils import MongoDB
from tests.utils.json_utils import YandexAPI


__author__ = 'lxz'


def get_name_weight(what_query, poi):
    poi_name = poi['name']
    splitted_name = split_string(poi_name)
    splitted_name.append(poi_name)
    full_weight = 0
    for name in splitted_name:
        if what_query.lower() == name.lower():
            full_weight += WEIGHT.NAME_EXACT_MATCH_WEIGHT
            break
        elif name.lower().startswith(what_query.lower()):
            full_weight += WEIGHT.NAME_LIKE_MATCH_WEIGHT + WEIGHT.SCORE_FOR_LIKE_MATCH_START_POS
            break
        elif name.lower().endswith(what_query.lower()):
            full_weight += WEIGHT.NAME_LIKE_MATCH_WEIGHT + WEIGHT.SCORE_FOR_LIKE_MATCH_END_POS
            break
        elif what_query.lower() in name.lower():
            full_weight += WEIGHT.NAME_LIKE_MATCH_WEIGHT
            break
        else:
            full_weight += 0
    return full_weight


def get_category_weight(what_query, poi):
    categories = MongoDB().get_categories(poi)
    #if what_query.lower() in [x.lower() for x in categories]:
    all_categories = [[y for y in x.split()] for x in categories]
    for category_terms in all_categories:
        for category_term in category_terms:
            if what_query.lower() in category_term:
                return WEIGHT.CATEGORY_EXACT_MATCH_WEIGHT
            elif any(x.lower().startswith(what_query.lower()) for x in categories):
                return WEIGHT.CATEGORY_LIKE_MATCH_WEIGHT + WEIGHT.SCORE_FOR_LIKE_MATCH_START_POS
            elif any(x.lower().endswith(what_query.lower()) for x in categories):
                return WEIGHT.CATEGORY_LIKE_MATCH_WEIGHT + WEIGHT.SCORE_FOR_LIKE_MATCH_END_POS
            elif any(what_query.lower() in x.lower() for x in categories):
                return WEIGHT.CATEGORY_LIKE_MATCH_WEIGHT
            else:
                return 0

#def get_category_weight(what_query, poi):
#    categories = MongoDB().get_categories(poi)
#    full_weight = 0
#    for category in categories:
#        if what_query.lower() == category.lower():
#            full_weight += WEIGHT.CATEGORY_EXACT_MATCH_WEIGHT
#            continue
#    #if what_query.lower() in [category.lower() for category in categories]:
#    #    return WEIGHT.CATEGORY_EXACT_MATCH_WEIGHT
#        elif any(x.lower().startswith(what_query.lower()) for x in categories):
#            full_weight += WEIGHT.CATEGORY_LIKE_MATCH_WEIGHT + WEIGHT.SCORE_FOR_LIKE_MATCH_START_POS
#            continue
#        elif any(x.lower().endswith(what_query.lower()) for x in categories):
#            full_weight += WEIGHT.CATEGORY_LIKE_MATCH_WEIGHT + WEIGHT.SCORE_FOR_LIKE_MATCH_END_POS
#            continue
#        elif any(what_query.lower() in x.lower() for x in categories):
#            full_weight += WEIGHT.CATEGORY_LIKE_MATCH_WEIGHT
#            continue
#        else:
#            full_weight += 0
#            continue
#    return full_weight


def get_amenity_weight(what_query, poi):
    amenities = MongoDB().get_amenities(poi)
    if what_query.lower() in [x.lower() for x in amenities]:
        return WEIGHT.AMENITY_EXACT_MATCH_WEIGHT
    elif any(what_query.lower() in x.lower() for x in amenities):
        return WEIGHT.AMENITY_LIKE_MATCH_WEIGHT
    else:
        return 0


def get_section_weight(what_query, poi):
    sections = MongoDB().get_sections(poi)
    if what_query.lower() in [x.lower() for x in sections]:
        return WEIGHT.SECTION_EXACT_MATCH_WEIGHT
    elif any(x.lower().startswith(what_query.lower()) for x in sections):
        return WEIGHT.SECTION_LIKE_MATCH_WEIGHT + WEIGHT.SCORE_FOR_LIKE_MATCH_START_POS
    elif any(x.lower().endswith(what_query.lower()) for x in sections):
        return WEIGHT.SECTION_LIKE_MATCH_WEIGHT + WEIGHT.SCORE_FOR_LIKE_MATCH_END_POS
    elif any(what_query.lower() in x.lower() for x in sections):
        return WEIGHT.SECTION_LIKE_MATCH_WEIGHT
    else:
        return 0


def distance_range(HB, LB, EP, SP, DP):
    k = Decimal(HB) - (Decimal(DP) - Decimal(SP)) * (Decimal(HB) - Decimal(LB)) / (Decimal(EP) - Decimal(SP))
    return Decimal(k)


def distance(sourceLatitude, sourceLongitude, targetLatitude, targetLongitude):
            longitudeDifference = targetLongitude - sourceLongitude
            a = math.radians(90 - sourceLatitude)
            c = math.radians(90 - targetLatitude)
            factor = (math.cos(a) * math.cos(c)) + (math.sin(a) * math.sin(c) * math.cos(math.radians(longitudeDifference)))

            if factor < -1:
                return math.pi * 6378137.0
            elif factor >= 1:
                return 0
            else:
                return math.acos(factor) * 6378137.0


def get_distance_weight(where_query, poi):
    where_coordinates = YandexAPI().get_coordinates(where_query)
    poi_coordinates = MongoDB().get_poi_by_id(str(poi['_id']))
    dist = distance(float(where_coordinates['lat']), float(where_coordinates['lon']), float(poi_coordinates['lat']), float(poi_coordinates['lon']))
    if WEIGHT.FIRST_DISTANCE_RANGE_MAX <= dist <= WEIGHT.FIRST_DISTANCE_RANGE_MIN:
        return distance_range(WEIGHT.FIRST_DISTANCE_POINT_MIN, WEIGHT.FIRST_DISTANCE_POINT_MAX, WEIGHT.FIRST_DISTANCE_RANGE_MIN, WEIGHT.FIRST_DISTANCE_RANGE_MAX, dist)
    elif WEIGHT.SECOND_DISTANCE_RANGE_MAX <= dist <= WEIGHT.SECOND_DISTANCE_RANGE_MIN:
        return distance_range(WEIGHT.SECOND_DISTANCE_POINT_MIN, WEIGHT.SECOND_DISTANCE_POINT_MAX, WEIGHT.SECOND_DISTANCE_RANGE_MIN, WEIGHT.SECOND_DISTANCE_RANGE_MAX, dist)
    elif WEIGHT.THIRD_DISTANCE_RANGE_MAX <= dist <= WEIGHT.THIRD_DISTANCE_RANGE_MIN:
        return distance_range(WEIGHT.THIRD_DISTANCE_POINT_MIN, WEIGHT.THIRD_DISTANCE_POINT_MAX, WEIGHT.THIRD_DISTANCE_RANGE_MIN, WEIGHT.THIRD_DISTANCE_RANGE_MAX, dist)
    else:
        return 0


def get_distance_real_weight(address, poi, N):
    return Decimal(get_distance_weight(address, poi)*12*Decimal(N)).quantize(Decimal('1.00'))


def check_all_weight(what_query, poi):
    if what_query == '':
        return 0
    splitted_what_query = split_string(what_query)
    splitted_what_query.append(what_query)
    full_weight = 0
    for x in splitted_what_query:
        name_weight = get_name_weight(x, poi)
        category_weight = get_category_weight(x, poi)
        amenity_weight = get_amenity_weight(x, poi)
        section_weight = get_section_weight(x, poi)
        full_weight += Decimal(name_weight + category_weight + amenity_weight + section_weight)
    return full_weight


def split_string(text):
    exactMatch = re.compile(ur"[\w']+", re.UNICODE)
    splitted_text = exactMatch.findall(text)
    return splitted_text

#def check_all_weight(what_query, poi):
#    if what_query == '':
#        return 0
#    name_weight = get_name_weight(what_query, poi)
#    category_weight = get_category_weight(what_query, poi)
#    amenity_weight = get_amenity_weight(what_query, poi)
#    section_weight = get_section_weight(what_query, poi)
#    return Decimal(name_weight + category_weight + amenity_weight + section_weight)

# print distance_range(WEIGHT.SECOND_DISTANCE_POINT_MIN, WEIGHT.SECOND_DISTANCE_POINT_MAX, WEIGHT.SECOND_DISTANCE_RANGE_MIN, WEIGHT.SECOND_DISTANCE_RANGE_MAX, 1504.27290438)*12

