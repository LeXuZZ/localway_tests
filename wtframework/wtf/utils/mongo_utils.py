# -*- coding: utf-8 -*-
from pymongo import MongoClient
from wtframework.wtf.config import ConfigReader

__author__ = 'lxz'


class MongoDB():

    localway_collection = None

    def __init__(self):
        info = ConfigReader('mongodb').get("mongodb_auth")
        conn = MongoClient(info)
        self.localway_collection = conn['localway']