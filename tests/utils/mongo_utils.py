# -*- coding: utf-8 -*-
from random import choice
from bson import ObjectId
from pymongo import MongoClient
from wtframework.wtf.config import ConfigReader

__author__ = 'lxz'


class MongoDB():
    localway_collection = None

    def __init__(self):
        info = ConfigReader('mongodb').get("mongodb_auth")
        conn = MongoClient(info)
        self.localway_collection = conn['localway']

    def get_poi_by_id(self, _id):
        return self.localway_collection.pois.find_one({"_id": ObjectId(_id)})

    get_random_poi = lambda self: choice([poi for poi in self.localway_collection.pois.find({"_id": {'$exists': True}})])

    def get_random_poi_with_cuisines(self):
        pois_with_cuisines = self.localway_collection.pois.find({"cuisines": {"$exists": True}})
        pois_with_cuisines_list = [poi for poi in pois_with_cuisines]
        random_poi = choice(pois_with_cuisines_list)
        return random_poi

    def get_random_poi_without_cuisines(self):
        pois_without_cuisines = self.localway_collection.pois.find({"cuisines": {"$exists": False}})
        pois_without_cuisines_list = [poi for poi in pois_without_cuisines]
        random_poi = choice(pois_without_cuisines_list)
        return random_poi

    def get_random_poi_with_hotel_stars_greater_than_0_and_check_io(self):
        hotel_pois = self.localway_collection.pois.find(
            {"sections": ObjectId("8af000000000000000000000"), 'hotelStars': {'$exists': True},
             'checkinTime': {'$exists': True}, 'checkoutTime': {'$exists': True}})
        hotel_pois_list = [poi for poi in hotel_pois]
        random_poi = choice(hotel_pois_list)
        return random_poi

    def get_random_poi_with_hotel_stars_equals_0_and_check_io_gt_0(self):
        hotel_pois = self.localway_collection.pois.find(
            {"sections": ObjectId("8af000000000000000000000"), 'hotelStars': {'$exists': False},
             'checkinTime': {'$gt': 0}, 'checkoutTime': {'$gt': 0}})
        hotel_pois_list = [poi for poi in hotel_pois]
        random_poi = choice(hotel_pois_list)
        return random_poi

    def get_random_poi_with_existing_coordinates(self):
        pois_with_coordinates = self.localway_collection.pois.find({"lon": {"$exists": True}, "lat": {"$exists": True}})
        pois_with_coordinates_list = [poi for poi in pois_with_coordinates]
        random_poi = choice(pois_with_coordinates_list)
        return random_poi

    def get_random_poi_without_existing_coordinates(self):
        pois_without_coordinates = self.localway_collection.pois.find(
            {"lon": {"$exists": False}, "lat": {"$exists": False}})
        pois_without_coordinates_list = [poi for poi in pois_without_coordinates]
        random_poi = choice(pois_without_coordinates_list)
        return random_poi

    def convert_amenity_id_to_name(self, object_id):
        amenities = self.localway_collection.amenities.find({"_id": ObjectId(object_id)})
        amenities_list = [x for x in amenities]
        return amenities_list[0]['name']

    def convert_category_id_to_name(self, object_id):
        categories = self.localway_collection.categories.find({"_id": ObjectId(object_id)})
        categories_list = [x for x in categories]
        return categories_list[0]['name']

    def convert_cuisine_id_to_name(self, object_id):
        cuisines = self.localway_collection.cuisines.find({"_id": ObjectId(object_id)})
        cuisines_list = [x for x in cuisines]
        return cuisines_list[0]['name']

    def convert_city_id_to_name(self, object_id):
        cities = self.localway_collection.cities.find({"_id": ObjectId(object_id)})
        cities_list = [x for x in cities]
        return cities_list[0]['name']

    def convert_metro_station_id_to_name(self, object_id):
        metro_stations = self.localway_collection.metro_stations.find({"_id": ObjectId(object_id)})
        metro_stations_list = [x for x in metro_stations]
        return metro_stations_list[0]['name']

    def convert_payments_id_to_name(self, object_id):
        payments = self.localway_collection.payments.find({"_id": ObjectId(object_id)})
        payments_list = [x for x in payments]
        return payments_list[0]['name']

    def convert_contact_type_id_to_name(self, object_id):
        contact = self.localway_collection.contact_types.find({"_id": ObjectId(object_id)})
        contact_list = [x for x in contact]
        return contact_list[0]['name']

    get_cuisines = lambda self, poi: sorted([self.convert_cuisine_id_to_name(str(x)) for x in poi['cuisines']])
    get_payments = lambda self, poi: sorted([self.convert_payments_id_to_name(str(x)) for x in poi['payments']])
    get_metro_stations = lambda self, poi: sorted([self.convert_metro_station_id_to_name(str(x)) for x in poi['metroStations']])
    get_amenities = lambda self, poi: sorted([self.convert_amenity_id_to_name(str(x)) for x in poi['amenities']])
    get_categories = lambda self, poi: sorted([self.convert_category_id_to_name(str(x)) for x in poi['categories']])