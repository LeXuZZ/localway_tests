import json
import re
import requests
from tests.static.constants import YANDEX_MAPS_API_REQUESTS
from wtframework.wtf.config import ConfigReader

__author__ = 'lxz'


class ElasticSearchAPI():
    def get_poi_json(self, poi_id):
        response = requests.get('http://172.31.237.13:9200/pois/poi/' + poi_id)
        return json.loads(response._content)['_source']


class SearchAPI():
    def get_response_only_what(self, query):
        return requests.get('http://172.31.237.13:8080/search-api/query?what=' + query)

    def get_response(self, what, where, page_size='25'):
        return requests.get('http://172.31.237.13:8080/search-api/query?sort=wordScore&sort.dir=desc&what=' + what + '&where=' + where + '&pageSize=' + page_size)

    def get_count_on_page(self, query):
        response = self.get_response_only_what(query)
        return json.loads(response._content)['countOnPage']

    def get_total_count(self, query):
        response = self.get_response_only_what(query)
        return json.loads(response._content)['totalCount']

    def get_items(self, what, where):
        response = self.get_response(what, where)
        return json.loads(response._content)['items']

    def get_viewed_together(self, poi_id):
        response = requests.get('http://172.31.237.13:8080/search-api/viewedTogether?excludeId=' + poi_id)
        return json.loads(response._content)


class YandexAPI():
    def get_response_from_api(self, query):
        response = requests.get(YANDEX_MAPS_API_REQUESTS.POI_COORDINATES.format(query))
        if response.status_code == 200:
            return response
        else:
            print 'Response status code ' + str(response.status_code) + '. Rejected.'
            return 0

    def get_found_count(self, query):
        response = self.get_response_from_api(query)
        return json.loads(response._content)['response']['GeoObjectCollection']['metaDataProperty'][
            'GeocoderResponseMetaData']['found']

    def get_coordinates(self, query):
        response = self.get_response_from_api(query)
        coor_string = json.loads(response._content)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        return {'lat': coor_string.split()[1], 'lon': coor_string.split()[0]}


class SectionAPI():
    def get_sections(self):
        response = requests.get('http://172.31.237.12/portal-api/site/meta/')
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