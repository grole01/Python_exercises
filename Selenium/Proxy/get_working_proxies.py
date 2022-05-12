import requests

def get_proxy_list():
    #proxy_list = requests.get('https://cdn.jsdelivr.net/gh/ShiftyTR/Proxy-List@master/https.txt').text.split('\n')
    proxy_list = requests.get('https://www.sslproxies.org/').text.split('\n')
    return proxy_list

def get_working_proxies(proxy_list):
    working = []
    for proxy in proxy_list:
        if proxy != '':
            try:
                r = requests.get('https://google.com/', proxies={'https': proxy}, timeout=3)
                if r.status_code == 200:
                    working.append(proxy)
                    print(f'{proxy} is working!')
                    print(working)
            except:
                print(f"{proxy} is not working.")
            pass

    return working

print(get_working_proxies(get_proxy_list()))