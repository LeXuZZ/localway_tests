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

    def get_random_poi_id_with_cuisines(self):
        pois_with_cuisines = self.localway_collection.pois.find({"cuisines": {"$exists": True}}, {"_id": "1"})
        pois_with_cuisines_list = [poi for poi in pois_with_cuisines]
        random_poi = choice(pois_with_cuisines_list)
        return random_poi['_id']

    def get_random_poi_id_without_cuisines(self):
        pois_without_cuisines = self.localway_collection.pois.find({"cuisines": {"$exists": False}}, {"_id": "1"})
        pois_without_cuisines_list = [poi for poi in pois_without_cuisines]
        random_poi = choice(pois_without_cuisines_list)
        return random_poi['_id']

    def get_poi_with_hotel_stars_and_check_io(self):
        hotel_pois = self.localway_collection.pois.find({"sections": ObjectId("8af000000000000000000000")}, {"_id": "1"})
        hotel_pois_list = [poi for poi in hotel_pois]
        random_poi = choice(hotel_pois_list)
        return random_poi['_id']