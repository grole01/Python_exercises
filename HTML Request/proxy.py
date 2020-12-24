import sys
from smartproxy.smartproxy import Requests
from pprint import pprint

r = Requests.request(request_type='get', url=('https://www.youtube.com'))
pprint(r.text)

#import proxyscrape

#collector = proxyscrape.create_collector('default', 'http')  # Create a collector for http resources
#proxy = collector.get_proxy({'country': 'united states'})  # Retrieve a united states proxy
#print(proxy)

#import proxyscrape
#from proxyscrape import create_collector, get_collector
#from pprint import pprint
#collector = create_collector('my-collector', ['socks4', 'socks5'])
#proxy = collector.get_proxies()
#pprint(proxy)

#from fp.fp import FreeProxy

#proxy1 = FreeProxy().get()
#proxy2 = FreeProxy(country_id=['US', 'BR'], timeout=0.3, rand=True).get()
#print(proxy1,proxy2)

#import requests
#from fp.fp import FreeProxy

#proxy = FreeProxy().get()

#r=requests.get("https://httpbin.org/ip",proxies={"http":proxy,"https":proxy},timeout=3)
#r=requests.get("https://www.google.com/",proxies={"http":proxy,"https":proxy},timeout=3)
#r = requests.get('https://websiteiwhantget', proxies={"http": proxy, "https": proxy},timeout=3)

#print(r.json)