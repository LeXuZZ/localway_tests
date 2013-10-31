from tests.utils.mongo_utils import MongoDB
from tests.utils.weight_util import distance
from wtframework.wtf.testobjects.basetests import WTFBaseTest

__author__ = 'lxz'


class Agglomeration(WTFBaseTest):
    maxDiff = None

    def test_agglomeration_distance(self):
        pois = MongoDB().get_pois_with_existing_coordinates()
        lat = 55.753676
        lon = 37.619899
        #for x in sorted([distance(lat, lon, float(x['lat']), float(x['lon'])) for x in pois]): print x
        for i, x in enumerate(sorted([x for x in pois], key=lambda recommended_poi: (distance(lat, lon, recommended_poi['lat'], recommended_poi['lon'])))): print str(i + 1) + ') ' + x['name'] + ' ' + str(x['_id']) + ' ' + str(distance(lat, lon, x['lat'], x['lon']))
        #for i, poi in enumerate(pois):
        #    print str(i + 1) + ') ' + str(distance(lat, lon, float(poi['lat']), float(poi['lon'])))
        pass