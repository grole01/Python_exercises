import requests
import json

url = 'https://www.zillow.com/search/GetSearchPageState.htm'
#url = 'https://www.zillow.com/community/providence/2078100258_zpid/'


headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'upgrade-insecure-requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

houses = []
for page in range(1, 4):
    params = {
        "searchQueryState": json.dumps({
            "pagination": {"currentPage": page},
            "usersSearchTerm": "35216",
            "mapBounds": {
                "west": -86.97413567189196,
                "east": -86.57244804982165,
                "south": 33.346263857015515,
                "north": 33.48754107532057
            },
            "mapZoom": 12,
            "regionSelection": [
                {
                    "regionId": 73386, "regionType": 7
                }
            ],
            "isMapVisible": True,
            "filterState": {
                "isAllHomes": {
                    "value": True
                },
                "sortSelection": {
                    "value": "globalrelevanceex"
                }
            },
            "isListVisible": True
        }),
        "wants": json.dumps(
            {
                "cat1": ["listResults", "mapResults"],
                "cat2": ["total"]
            }
        ),
        "requestId": 3
    }

    # send request
    page = requests.get(url, headers=headers, params=params)

    # get json data
    json_data = page.json()

    # loop via data
    for house in json_data['cat1']['searchResults']['listResults']:
        houses.append(house)


# show data
print('Total houses - {}'.format(len(houses)))

# show info in houses
for house in houses:

    if 'brokerName' in house.keys():
        print('{}: {}'.format(house['brokerName'], house['price']))
    else:
        print('No broker: {}'.format(house['price']))
    '''
    if 'brokerPhoneNumber' in house.keys():
        print('{}: {}'.format(house['brokerPhoneNumber'], house['price']))
    else:
        print('No broker: {}'.format(house['price']))
    '''