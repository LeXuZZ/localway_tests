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