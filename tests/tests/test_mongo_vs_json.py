import unittest
import json
from tests.utils.mongo_utils import MongoDB, MongoEncoder
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from tests.utils.json_utils import POI_JSON

__author__ = 'lxz'


class MongoVsJSON(WTFBaseTest):

    maxDiff = None

    # def test_mongo_vs_json(self):
    #     poi = MongoDB().get_poi_by_id('172772af0000000000000000')
    #     poi_json = POI_JSON('172772af0000000000000000')._json
    #     poi_converted = json.loads(MongoEncoder().encode(poi))
    #     self.assertDictEqual(poi_converted, poi_json)

if __name__ == "__main__":
    unittest.main()