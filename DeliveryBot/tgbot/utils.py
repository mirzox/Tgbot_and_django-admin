import http.client
import urllib.parse
from .const import LOCATION_API_TOKEN
import json


def request(lat, lon):
    conn = http.client.HTTPConnection('api.positionstack.com')

    params = urllib.parse.urlencode({
        'access_key': LOCATION_API_TOKEN,
        'query': f'{lat},{lon}',
        })
    conn.request('GET', '/v1/reverse?{}'.format(params))

    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)['data'][0]
    result = f"Улица {data['street']}, город {data['region']}, страна {data['country']}"
    return result
