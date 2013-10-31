from collections import defaultdict
import pprint
from tests.static.sql_queries import POSTGRE_SQL_QUERIES
from tests.utils.data_utils import query_format
from tests.utils.json_utils import YandexAPI
from wtframework.wtf.config import ConfigReader

__author__ = 'lxz'
import psycopg2
from psycopg2 import extras


class PostgreSQL():

    conn = None

    def __init__(self):
        cr = ConfigReader('db')
        self.conn = psycopg2.connect(dbname=cr.get("postgre_dbname"), user=cr.get("postgre_user"), host=cr.get("postgre_host"), port=cr.get("postgre_port"), password=cr.get("postgre_password"))
        self.cur = self.conn.cursor(cursor_factory=extras.RealDictCursor)

    def get_current_revision_info_by_place_id(self, place_id):
        self.cur.execute(query_format(place_id, POSTGRE_SQL_QUERIES.CURRENT_REVISION_INFO_BY_PLACE_ID))
        response = self.cur.fetchone()
        return response

    def get_city_name_by_city_id(self, city_id):
        self.cur.execute(query_format(city_id, POSTGRE_SQL_QUERIES.NAME_BY_CITY_ID))
        response = self.cur.fetchone()
        return response['name']

    def get_metro_names_by_place_id(self, place_id):
        self.cur.execute(query_format(place_id, POSTGRE_SQL_QUERIES.METRO_NAMES_BY_PLACE_ID))
        response = self.cur.fetchall()
        return [x['name'].decode("utf-8") for x in response]

    def get_region_name_by_place_id(self, place_id):
        self.cur.execute(query_format(place_id, POSTGRE_SQL_QUERIES.REGION_NAME_BY_PLACE_ID))
        response = self.cur.fetchone()
        return response['name']

    def get_prefix_name_by_city_id(self, city_id):
        self.cur.execute(query_format(city_id, POSTGRE_SQL_QUERIES.PREFIX_NAME_BY_CITY_ID))
        response = self.cur.fetchone()
        return response['name']

    def get_prefix_short_name_by_city_id(self, city_id):
        self.cur.execute(query_format(city_id, POSTGRE_SQL_QUERIES.PREFIX_SHORT_NAME_BY_CITY_ID))
        response = self.cur.fetchone()
        return response['short_name']

    def get_category_names_and_priorities_by_place_id(self, place_id):
        self.cur.execute(query_format(place_id, POSTGRE_SQL_QUERIES.CATEGORY_NAMES_AND_PRIORITIES_BY_PLACE_ID))
        response = self.cur.fetchall()
        cat = []
        for data in response:
            cat.append(dict(name=data['name'].decode("utf-8"), priority=data['priority']))
        return cat

    def get_all_pois_without_geo_data(self):
        self.cur.execute(POSTGRE_SQL_QUERIES.GET_ALL_POI_ID_WITHOUT_GEO_DATA)
        response = self.cur.fetchall()
        return [x for x in response]

    def set_all_geo(self):
        all_pois = self.get_all_pois_without_geo_data()
        for i in all_pois:
            address = i['address']
            _id = i['id']
            coordinates = YandexAPI.get_coordinates(address)
            if coordinates == 0:
                print 'Wrong Yandex response for ' + str(_id)
                continue
            print str(_id) + ' ' + str(address) + ' lat = ' + str(coordinates['lat']) + ' lon = ' + str(coordinates['lon'])
            query = 'UPDATE place_revision SET latitude=' + str(coordinates['lat']) + ', longitude=' + str(coordinates['lon']) + ' WHERE id=' + str(_id)
            self.cur.execute(query)
            self.conn.commit()
            print 'Done for id ' + str(_id)
            self.cur.execute(query)

    def get_all_cities_without_geo(self):
        self.cur.execute(POSTGRE_SQL_QUERIES.CITY_ADDRESSES_WITHOUT_GEO_DATA)
        response = self.cur.fetchall()
        return [x for x in response]

    def set_all_cities_geo(self):
        all_cities = self.get_all_cities_without_geo()
        counter = 0
        for i in all_cities:
            address = i['address']
            _id = i['id']
            coordinates = YandexAPI.get_coordinates(address)
            if coordinates == 0:
                # print 'Not in moscow ' + str(_id)
                continue
            counter += 1
            print str(counter) + ' ' + str(_id) + ' ' + str(address) + ' lat = ' + str(coordinates['lat']) + ' lon = ' + str(coordinates['lon'])


PostgreSQL().set_all_cities_geo()
print 'Done!'