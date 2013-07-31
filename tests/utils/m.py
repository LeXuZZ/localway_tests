from tests.utils.mongo_utils import MongoDB

for i in range(50):
    poi = MongoDB().get_random_poi()
    print poi['_id']
