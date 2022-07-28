from lxml import html
import requests
import unicodecsv as csv
import argparse
import json
from bs4 import BeautifulSoup
#import pandas


def clean(text):
    if text:
        return ' '.join(' '.join(text).split())
    return None


def get_headers():
    # Creating headers.
    '''
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.8',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }
    return headers
    '''

    headers = {
        'authority': 'www.zillow.com',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hr-HR;q=0.7,hr;q=0.6',
        'cache-control': 'no-cache',
        # Requests sorts cookies= alphabetically
        # 'cookie': f"_ga=GA1.2.113295374.1648806787; zg_anonymous_id=%225bc0abd2-2b35-4a59-8169-d0db205669f2%22; zjs_anonymous_id=%229d3a0b1e-0b8d-4b34-93b9-e7f090c85b20%22; _pxvid=88fd5cf1-b1a1-11ec-b0be-76495a594c64; __pdst=f0b87afed64741cbb868842252c5e280; _cs_c=0; _pin_unauth=dWlkPU56STROVGs0WmpVdFlUVTFNeTAwWVRBd0xXSmpaV010TVRJd05EZzRaakpoTXpFeg; g_state={\"i_l\":0}; loginmemento=1|e648d393a03cc20d828750eb48758c21bb72919e99d4c1fceaaa7bbfcc3afcd6; userid=X|3|5a8202f2f6380c19%7C5%7CFlhKs2i6OA7DQRxaIXkxM0rWvN7DAwAI; zjs_user_id=%22X1-ZUs8zz494u1fyh_2jaye%22; optimizelyEndUserId=oeu1648806904677r0.004723879626656657; _hp2_id.1215457233=%7B%22userId%22%3A%223975453180120533%22%2C%22pageviewId%22%3A%222258486643294492%22%2C%22sessionId%22%3A%224748313794875801%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _cs_id=e9a054b0-46cd-a341-ae9b-203c87fbc702.1648806789.5.1649067389.1649067389.1.1682970789718; zguid=24|%249d3a0b1e-0b8d-4b34-93b9-e7f090c85b20; _gcl_au=1.1.1922716115.1656662322; _derived_epik=dj0yJnU9Y1FxTWNHMS1HamFkQ1pwTjFmM2FtNEN5WWFVUzBnOGgmbj03SVpGUlZFN3Q2Rk51bU0tekJaU0VBJm09NCZ0PUFBQUFBR0stcXNZJnJtPTQmcnQ9QUFBQUFHSy1xc1k; _gid=GA1.2.1317390603.1658137895; KruxPixel=true; KruxAddition=true; zgsession=1|0ea503e0-a39f-4f19-83e5-5231531cd2b0; pxcts=38d24a5d-0686-11ed-88ad-6a6b486a7952; DoubleClickSession=true; JSESSIONID=D00A3189FFC37B9B7AC93827D7142013; ZILLOW_SID=1|AAAAAVVbFRIBVVsVEvuY7oMN5Mf8ZiMffwhs%2FfvUWecB6OE7E%2FWfHg6fZFNQPwwEYVZJRZfG%2BX24pQnlnd4TO6qwSxlq; _px3=60dda8d9d0935dc5d5fe23613f139caec4c11dac5102fea789cd6c7faba2b1b4:Lt/RwlFGKj8W0VFmCh5fTGCguqDg8rkKhAkLAb+P06BBbrbPEcRAscQ70qM6CoWMngXQBPOx7KqrC2pI1T00rw==:1000:jVh8oDW6i9A8fAclkm4RnV7crmmfFeiIh0h05Pe24C2ImOxD7eV74DLShpXAn0xID7lm92bJ9jd09jIB0MSPjXKl367kXhG3Pectv72jRaMuR8Gua68IfvTdm7/mQiMaPvmjqZPgMTijZOz4sJwX2FpX46LDZg4dP5q1h5EDPlzK4qTsYbrULFP+INzlmSkds5vFFCGaGGvzYwSI/vRrpw==; _uetsid=46e4f060068511edb892db448de95a36; _uetvid=892624d0b1a111ec926bc1d6f2699abd; utag_main=v_id:017fe48afedd000f5b5db368223005072001706a0086e{_sn:35$_se:1$_ss:1$_st:1658231682448$dc_visit:30$ses_id:1658229882448%3Bexp-session$_pn:1%3Bexp-session;} _clck=1idbk78|1|f3a|0; _clsk=jcf5v2|1658229936180|2|0|l.clarity.ms/collect; AWSALB=zCWSpCqj2EzLMurs1N0mHPbyxAYGJj73I9HsvgW4I7rhPEmZtl20IqS7VlXqvnA5AKH2r6LMC7pipynzIaAYHalNYWdVmQCkNKHss4J1ueB3sWl5ERZ4xFOncqmw; AWSALBCORS=zCWSpCqj2EzLMurs1N0mHPbyxAYGJj73I9HsvgW4I7rhPEmZtl20IqS7VlXqvnA5AKH2r6LMC7pipynzIaAYHalNYWdVmQCkNKHss4J1ueB3sWl5ERZ4xFOncqmw; search=6|1660821937626%7Cregion%3Dchicago-il-60615%26rect%3D41.817078%252C-87.56441%252C41.786128%252C-87.626032%26disp%3Dmap%26mdm%3Dauto%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%09%0984617%09%09%09%09%09%09; _gat=1; _pxff_bsco=1",
        'pragma': 'no-cache',
        'referer': 'https://www.zillow.com/chicago-il-60615/?fromHomePage=true&shouldFireSellPageImplicitClaimGA=false&fromHomePageTab=buy&searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%2260615%22%2C%22mapBounds%22%3A%7B%22west%22%3A-87.64809270410156%2C%22east%22%3A-87.54234929589843%2C%22south%22%3A41.77024547240333%2C%22north%22%3A41.8329489252935%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A84617%2C%22regionType%22%3A7%7D%5D%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
    return headers

def create_url(zipcode, filter):
    # Creating Zillow URL based on the filter.

    if filter == "newest":
        url = "https://www.zillow.com/homes/for_sale/{0}/0_singlestory/days_sort".format(zipcode)
    elif filter == "cheapest":
        url = "https://www.zillow.com/homes/for_sale/{0}/0_singlestory/pricea_sort/".format(zipcode)
    else:
        url = "https://www.zillow.com/homes/for_sale/{0}_rb/?fromHomePage=true&shouldFireSellPageImplicitClaimGA=false&fromHomePageTab=buy".format(zipcode)
    print(url)
    return url


def save_to_file(response):
    # saving response to `response.html`

    with open("response.html", 'w', encoding="utf-8") as fp:
        fp.write(response.text)


def write_data_to_csv(data):
    # saving scraped data to csv.

    with open("properties-%s.csv" % (zipcode), 'wb') as csvfile:
        fieldnames = ['title', 'address', 'city', 'state', 'postal_code', 'price', 'facts and features', 'real estate provider', 'url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
            print(row)


def get_response(url):
    # Getting response from zillow.com.

    for i in range(5):
        response = requests.get(url, headers=get_headers())
        print("status code received:", response.status_code)
        if response.status_code != 200:
            # saving response to file for debugging purpose.
            save_to_file(response)
            continue
        else:
            save_to_file(response)
            return response
    return None

def get_data_from_json(raw_json_data):
    # getting data from json (type 2 of their A/B testing page)
    cleaned_data = clean(raw_json_data).replace('<!--', "").replace("-->", "")
    properties_list = []

    try:
        json_data = json.loads(cleaned_data)
        #search_results = json_data.get('searchResults').get('listResults', [])
        search_results = json_data.get('cat1').get('searchResults').get('listResults', [])

        for properties in search_results:
            #address = properties.get('addressWithZip')streetAddress
            property_info = properties.get('hdpData', {}).get('homeInfo')
            address = property_info.get('streetAddress')
            city = property_info.get('city')
            state = property_info.get('state')
            postal_code = property_info.get('zipcode')
            price = properties.get('price')
            bedrooms = properties.get('beds')
            bathrooms = properties.get('baths')
            area = properties.get('area')
            info = f'{bedrooms} bds, {bathrooms} ba ,{area} sqft'
            broker = properties.get('brokerName')
            property_url = properties.get('detailUrl')
            title = properties.get('statusText')

            data = {'address': address,
                    'city': city,
                    'state': state,
                    'postal_code': postal_code,
                    'price': price,
                    'facts and features': info,
                    'real estate provider': broker,
                    'url': property_url,
                    'title': title}
            print(data)
            properties_list.append(data)

        return properties_list

    except ValueError:
        print("Invalid json")
        return None


def parse(zipcode, filter=None):
    url = create_url(zipcode,filter)
    print(url)
    response = get_response(url)

    if not response:
        print("Failed to fetch the page, please check `response.html` to see the response received from zillow.com.")
        return None

    #parser = html.fromstring(response.text)
    response = BeautifulSoup(requests.get(url, headers=get_headers()).content, "html5lib")
    search_results = response.find("//div[@id='search-results']//article")


    if not search_results:
        print("parsing from json data")
        # identified as type 2 page
        #raw_json_data = parser.xpath('//script[@data-zrr-shared-data-key="mobileSearchPageStore"]//text()')
        raw_json_data = response.find("script", {"data-zrr-shared-data-key": "mobileSearchPageStore"})
        return get_data_from_json(raw_json_data)

    print("parsing from html page")
    properties_list = []
    for properties in search_results:
        raw_address = properties.xpath(".//span[@itemprop='address']//span[@itemprop='streetAddress']//text()")
        raw_city = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressLocality']//text()")
        raw_state = properties.xpath(".//span[@itemprop='address']//span[@itemprop='addressRegion']//text()")
        raw_postal_code = properties.xpath(".//span[@itemprop='address']//span[@itemprop='postalCode']//text()")
        raw_price = properties.xpath(".//span[@class='zsg-photo-card-price']//text()")
        raw_info = properties.xpath(".//span[@class='zsg-photo-card-info']//text()")
        raw_broker_name = properties.xpath(".//span[@class='zsg-photo-card-broker-name']//text()")
        url = properties.xpath(".//a[contains(@class,'overlay-link')]/@href")
        raw_title = properties.xpath(".//h4//text()")

        address = clean(raw_address)
        city = clean(raw_city)
        state = clean(raw_state)
        postal_code = clean(raw_postal_code)
        price = clean(raw_price)
        info = clean(raw_info).replace(u"\xb7", ',')
        broker = clean(raw_broker_name)
        title = clean(raw_title)
        property_url = "https://www.zillow.com" + url[0] if url else None
        is_forsale = properties.xpath('.//span[@class="zsg-icon-for-sale"]')

        properties = {'address': address,
                      'city': city,
                      'state': state,
                      'postal_code': postal_code,
                      'price': price,
                      'facts and features': info,
                      'real estate provider': broker,
                      'url': property_url,
                      'title': title}
        if is_forsale:
            properties_list.append(properties)
            print(len(properties_list))
    return properties_list


if __name__ == "__main__":
    # Reading arguments

    argparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    argparser.add_argument('zipcode', help='')
    #argparser.add_argument('21456446_zpid', help='')

    sortorder_help = """
    available sort orders are :
    newest : Latest property details,
    cheapest : Properties with cheapest price
    """

    argparser.add_argument('sort', nargs='?', help=sortorder_help, default='Homes For You')
    args = argparser.parse_args()
    zipcode = args.zipcode
    sort = args.sort
    print ("Fetching data for %s" % (zipcode))
    scraped_data = parse(zipcode, sort)
    if scraped_data:
        print ("Writing data to output file")
        write_data_to_csv(scraped_data)
