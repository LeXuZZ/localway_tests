# coding=utf-8
__author__ = 'lxz'


class POI_KEYS():
    NAME = 'name'
    DESCRIPTION = 'description'
    INTRO = 'intro'
    RATING = 'rating'
    CITY = 'city'
    STREET = 'street'
    BUILDING = 'building'
    HOUSE = 'house'
    IMAGES = 'images'
    CATEGORIES = 'categories'
    AMENITIES = 'amenities'
    METRO_STATIONS = 'metroStations'
    PAYMENTS = 'payments'
    CONTACTS = 'contacts'
    CONTACT = 'contact'
    CONTACT_TYPE = 'contactType'
    WORK_TIME = 'groupedSchedule'
    AROUND_THE_CLOCK = 'aroundTheClock'
    AVERAGE_PRICE = 'averagePrice'
    BUSINESS_LUNCH_PRICE = 'businessLunchPrice'
    CUISINES = 'cuisines'
    LATITUDE = 'lat'
    LONGITUDE = 'lon'
    CHECK_IN_TIME = 'checkinTime'
    CHECK_OUT_TIME = 'checkoutTime'

class CONTACT_KEYS():
    PHONE = 'Телефон'
    EMAIL = 'EMail'
    SITE = 'Сайт'
    TWITTER = 'twitter'
    VK = 'vk.com'
    FACEBOOK = 'facebook'


class SECTION_LINKS_SUFFIX():
    LEISURE = 'ng/#/section/leisure'
    ACTIVE = 'ng/#/section/active'
    RESTAURANTS = 'ng/#/section/restaurants'
    HOTELS = 'ng/#/section/hotels'
    JOURNEYS = 'ng/#/section/journeys'


class URL_PREFIXES():
    POI_ID_PREFIX = '#/poi?id='


class WEIGHT:
    SCORE_FOR_EXACT_MATCH = 1
    SCORE_FOR_LIKE_MATCH = 0.3

    ADDRESS_WEIGHT = 12
    NAME_WEIGHT = 10
    CATEGORY_WEIGHT = 8
    AMENITY_WEIGHT = 6
    SECTION_WEIGHT = 4

    NAME_EXACT_MATCH_WEIGHT = NAME_WEIGHT * SCORE_FOR_EXACT_MATCH
    NAME_LIKE_MATCH_WEIGHT = NAME_WEIGHT * SCORE_FOR_LIKE_MATCH

    CATEGORY_EXACT_MATCH_WEIGHT = CATEGORY_WEIGHT * SCORE_FOR_EXACT_MATCH
    CATEGORY_LIKE_MATCH_WEIGHT = CATEGORY_WEIGHT * SCORE_FOR_LIKE_MATCH

    SECTION_EXACT_MATCH_WEIGHT = SECTION_WEIGHT * SCORE_FOR_EXACT_MATCH
    SECTION_LIKE_MATCH_WEIGHT = SECTION_WEIGHT * SCORE_FOR_LIKE_MATCH

    AMENITY_EXACT_MATCH_WEIGHT = AMENITY_WEIGHT * SCORE_FOR_EXACT_MATCH
    AMENITY_LIKE_MATCH_WEIGHT = 0

    FIRST_DISTANCE_RANGE_MIN = 500.0
    FIRST_DISTANCE_RANGE_MAX = 0.0
    FIRST_DISTANCE_POINT_MIN = 1.0
    FIRST_DISTANCE_POINT_MAX = 0.9

    SECOND_DISTANCE_RANGE_MIN = 2000.0
    SECOND_DISTANCE_RANGE_MAX = 500.001
    SECOND_DISTANCE_POINT_MIN = 0.9
    SECOND_DISTANCE_POINT_MAX = 0.75

    THIRD_DISTANCE_RANGE_MIN = 15000
    THIRD_DISTANCE_RANGE_MAX = 2000.001
    THIRD_DISTANCE_POINT_MIN = 0.75
    THIRD_DISTANCE_POINT_MAX = 0.0


class YANDEX_MAPS_API_REQUESTS():

    POI_COORDINATES = 'http://geocode-maps.yandex.ru/1.x/?geocode=WHERE&kind=house&format=json&rspn=1&spn=0.47795,0.33855&results=1&ll=37.61776155,55.755773'

class TEST_POI_ID:

    POI_ID_FOR_PHOTO_GALLERY = '169085af0000000000000000'