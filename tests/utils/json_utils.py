# coding=utf-8
import json
import re
import requests
from tests.static.constants import YANDEX_MAPS_API_REQUESTS
from wtframework.wtf.config import ConfigReader

__author__ = 'lxz'


class ElasticSearchAPI():
    def __init__(self):
        pass

    def get_poi_json(self, poi_id):
        response = requests.get('http://172.31.237.13:9200/pois/poi/' + poi_id)
        return json.loads(response._content)['_source']


class SearchAPI():
    def __init__(self):
        pass

    @staticmethod
    def get_response_only_what(query):
        return requests.get(
            ConfigReader('site_credentials').get("elastic_search_server_url") + 'search-api/query?what=' + query)

    @staticmethod
    def get_response(what, where, page_size='25', categories='', amenities='', sort_type='wordScore', sort_dir='desc',
                     agglomeration='1af000000000000000000000'):
        return requests.get(ConfigReader('site_credentials').get(
            "elastic_search_server_url") + 'search-api/query?sort=' + sort_type + '&sort.dir=' + sort_dir + '&agglomeration=' + agglomeration + '&what=' + what + '&where=' + where + '&pageSize=' + page_size + ''.join(
            ['&categoryName=' + cat for cat in categories]) + ''.join(
            ['&amenityName=' + amenity for amenity in amenities]))

    @staticmethod
    def get_count_on_page(query):
        response = SearchAPI.get_response_only_what(query)
        return json.loads(response._content)['countOnPage']

    @staticmethod
    def get_total_count(what='', where='', page_size='25', categories='', amenities='', sort_type='wordScore',
                        sort_dir='desc', agglomeration='1af000000000000000000000'):
        response = SearchAPI.get_response(what, where, page_size, categories, amenities, sort_type, sort_dir, agglomeration)
        return json.loads(response._content)['totalCount']

    @staticmethod
    def get_total_count_by_primary_search(what='', where='', page_size='25', categories='', amenities='',
                                          sort_type='wordScore', sort_dir='desc', agglomeration='1af000000000000000000000'):
        response = SearchAPI.get_response(what, where, page_size, categories, amenities, sort_type, sort_dir, agglomeration)
        return json.loads(response._content)['totalCountByPrimarySearch']

    @staticmethod
    def get_items(what='', where='', page_size='25', categories='', amenities='', sort_type='wordScore',
                  sort_dir='desc', agglomeration='1af000000000000000000000'):
        response = SearchAPI.get_response(what, where, page_size, categories, amenities, sort_type, sort_dir, agglomeration)
        return json.loads(response._content)['items']

    @staticmethod
    def get_viewed_together(poi_id):
        response = requests.get(ConfigReader('site_credentials').get(
            "elastic_search_server_url") + 'search-api/viewedTogether?excludeId=' + poi_id)
        return json.loads(response._content)

    @staticmethod
    def chain_names(names):
        result = ''
        for i, name in enumerate(names):
            result += name
            if i != len(names) - 1:
                result += '__'
        return result


class YandexAPI():
    def __init__(self):
        pass

    @staticmethod
    def get_response_from_api(query):
        response = requests.get(re.sub('WHERE', query, YANDEX_MAPS_API_REQUESTS.POI_COORDINATES))
        if response.status_code == 200:
            return response
        else:
            # print 'Response status code ' + str(response.status_code) + '. Rejected.'
            return 0

    @staticmethod
    def get_found_count(query):
        response = YandexAPI.get_response_from_api(query)
        return json.loads(response._content)['response']['GeoObjectCollection']['metaDataProperty'][
            'GeocoderResponseMetaData']['found']

    @staticmethod
    def get_coordinates(query):
        response = YandexAPI.get_response_from_api(query)
        try:
            coor_string = \
                json.loads(response._content)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
                    'Point'][
                    'pos']
        except IndexError:
            # print query
            # print json.loads(response._content)
            return 0
        return {'lat': coor_string.split()[1], 'lon': coor_string.split()[0]}


class SectionAPI():
    def __init__(self):
        pass

    @staticmethod
    def get_sections():
        response = requests.get(ConfigReader('site_credentials').get('default_url') + 'portal-api/site/meta/')
        return json.loads(response._content)


class PortalAPI:
    def __init__(self):
        pass

    @staticmethod
    def get_config_for_around_poi():
        response = requests.get(ConfigReader('site_credentials').get('default_url') + 'portal-api/system/getConfig')
        return json.loads(response._content)


class POI_JSON():
    _json = None

    def __init__(self, poi_id):
        self._json = requests.get(
            ConfigReader('site_credentials').get("default_url") + "portal-api/poi/" + poi_id).json()

    @property
    def id(self):
        return self._json['_id']

    @property
    def amenities(self):
        return self._json['amenities']

    @property
    def average_price(self):
        return self._json['averagePrice']

    @property
    def business_lunch_price(self):
        return self._json['businessLunchPrice']

    @property
    def categories(self):
        return self._json['categories']

    @property
    def city(self):
        return self._json['city']

    @property
    def contacts(self):
        return self._json['contacts']

    @property
    def cuisines(self):
        return self._json['cuisines']

    @property
    def description(self):
        return self._json['description']

    @property
    def district(self):
        return self._json['district']

    @property
    def grouped_schedule(self):
        return self._json['groupedSchedule']

    @property
    def hotel_stars(self):
        return self._json['hotelStars']

    @property
    def house(self):
        return self._json['house']

    @property
    def images(self):
        return self._json['images']

    @property
    def lat(self):
        try:
            return self._json['lat']
        except KeyError:
            return None

    @property
    def lon(self):
        try:
            return self._json['lon']
        except KeyError:
            return None

    @property
    def metro_stations(self):
        return self._json['metroStations']

    @property
    def name(self):
        return self._json['name']

    @property
    def payments(self):
        return self._json['payments']

    @property
    def rating(self):
        return self._json['rating']

    @property
    def sections(self):
        return self._json['sections']

    @property
    def street(self):
        return self._json['street']