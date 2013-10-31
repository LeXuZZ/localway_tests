__author__ = 'lxz'


class POSTGRE_SQL_QUERIES():
    METRO_NAMES_BY_PLACE_ID = 'SELECT ms.name ' \
                              'FROM place_revision as pr ' \
                              'JOIN place_revision__metro_station as prms ON pr.id=prms.place_revision_id ' \
                              'JOIN metro_station as ms ON prms.metro_station_id=ms.id ' \
                              'WHERE pr.place_id=QUERY_TEXT AND is_current_version = True'

    REGION_NAME_BY_PLACE_ID = 'SELECT ct1.name ' \
                              'FROM place_revision as pr ' \
                              'JOIN city as ct ON pr.city_id = ct.id ' \
                              'JOIN city as ct1 ON ct1.id=ct.region_id ' \
                              'WHERE pr.place_id=QUERY_TEXT AND is_current_version = True'

    NAME_BY_CITY_ID = 'SELECT name FROM city WHERE id=QUERY_TEXT'

    CURRENT_REVISION_INFO_BY_PLACE_ID = 'SELECT * FROM place_revision WHERE place_id=QUERY_TEXT AND is_current_version = True'

    PREFIX_NAME_BY_CITY_ID = 'SELECT ct.name FROM city as c JOIN city_type as ct ON c.city_type_id=ct.id WHERE c.id=QUERY_TEXT'

    PREFIX_SHORT_NAME_BY_CITY_ID = 'SELECT ct.short_name FROM city as c JOIN city_type as ct ON c.city_type_id=ct.id WHERE c.id=QUERY_TEXT'

    CATEGORY_NAMES_AND_PRIORITIES_BY_PLACE_ID = 'SELECT cat.name, prc.priority FROM place_revision as pr JOIN place_revision__category as prc ON pr.id=prc.place_revision_id JOIN category as cat ON prc.category_id=cat.id WHERE pr.place_id=QUERY_TEXT AND pr.is_current_version = True'

    GET_ALL_POI_ID_WITHOUT_GEO_DATA = 'SELECT pr.id, pr.street, concat(ct.short_name, \' \', c.name, \', \', pr.street, \', \', pr.house, \' \', pr.building) as address FROM place_revision as pr JOIN city as c ON c.id=pr.city_id JOIN city_type as ct ON ct.id=c.city_type_id WHERE pr.is_current_version = True AND (pr.latitude is NULL OR pr.longitude IS NULL) AND pr.city_id is not NULL '

    CITY_ADDRESSES_WITHOUT_GEO_DATA = 'SELECT c1.id, c.name, ct.short_name, ct1.short_name, c1.name, c1.zipcode, concat(c.name, \' \', ct.short_name, \', \', ct1.short_name, \' \', c1.name) as address FROM city as c JOIN city as c1 ON c.id=c1.region_id JOIN city_type as ct ON ct.id=c.city_type_id JOIN city_type as ct1 ON ct1.id=c1.city_type_id WHERE c1.latitude is NULL OR c1.longitude IS NULL'