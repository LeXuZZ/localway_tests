__author__ = 'lxz'
import requests, json, re

resp = requests.get('http://staging.localway.ru/search-api/query?offset=1&pageSize=10000')
items = json.loads(resp.content)['items']
items_length = len(items)
for i, item in enumerate(items):
    poi_resp = requests.get('http://staging.localway.ru/portal-api/poi/' + item['_id'])
    poi = json.loads(poi_resp.content)
    if poi['contacts']:
        for contact in poi['contacts']:
            if contact['contactType'] == u'7af000000000000000000000':
                rg = re.search('[^/]+$', contact['contact'])
                if rg:
                    var1 = rg.group(0)
                    url = 'http://graph.facebook.com/' + var1
                    resp = requests.get(url)
                    if resp.status_code == 200:
                        try:
                            fb_graph_content = json.loads(resp.content)
                            if 'likes' in fb_graph_content:
                                print '[' + str(round(float(i) / float(items_length) * 100, 2)) + '% done!] POI name: ' + poi[
                                    'name'] + ' with id: ' + poi['_id'] + ' has ' + str(
                                    fb_graph_content['likes']) + ' likes'
                        except ValueError:
                            continue
