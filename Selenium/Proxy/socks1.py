import requests
from bs4 import BeautifulSoup as soup
from itertools import cycle

url = 'https://www.socks-proxy.net/'
response = requests.get(url)
bsobj = soup(response.content,'lxml')
proxies= set()
for ip in bsobj.findAll('table')[0].findAll('tbody')[0].findAll('tr'):
  cols = ip.findChildren(recursive = False)
  cols = [element.text.strip() for element in cols]
  #print(cols)
  proxy = ':'.join([cols[0],cols[1]])
  proxy = 'socks4://'+proxy
  proxies.add(proxy)
  #



  # If you are copy pasting proxy ips, put in the list below
  # proxies = ['121.129.127.209:80', '124.41.215.238:45169', '185.93.3.123:8080', '194.182.64.67:3128', '106.0.38.174:8080', '163.172.175.210:3128', '13.92.196.150:8080']
  proxy_pool = cycle(proxies)
  url = 'https://httpbin.org/ip'
  for i in range(1, 10):
    # Get a proxy from the pool
    proxy = next(proxy_pool)
    print("Request #%d" % i)
    try:
      response = requests.get(url, proxies={"http": proxy, "https": proxy})
      print(response)#.json())
      print(proxy)
    except:
      # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
      # We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url
      print("Skipping. Connnection error")