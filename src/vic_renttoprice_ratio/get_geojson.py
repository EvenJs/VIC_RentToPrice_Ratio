import requests
from requests.exceptions import RequestException


url = 'https://data.gov.au/geoserver/vic-suburb-locality-boundaries-psma-administrative-boundaries/wfs?request=' \
      'GetFeature&typeName=ckan_af33dd8c_0534_4e18_9245_fc64440f742e&outputFormat=json'


def get_geojson(url_link):
    try:
        res = requests.get(url_link)
        if res.status_code == 200:
            vic_map = res.json()
            return vic_map
        return None
    except RequestException:
        return None


if __name__ == "__main__":
    get_geojson(url)
