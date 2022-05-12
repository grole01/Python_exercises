import os
import zipfile
import undetected_chromedriver.v2 as uc
import time
'''
PROXY_HOST = '107.23.19.8'  # rotating proxy
PROXY_PORT = 3135
PROXY_USER = 'ggwp'
PROXY_PASS = 'ggwp123'

host = '107.23.19.8'
port = 3135
username = 'ggwp'
password = 'ggwp123'
'''
PROXY_HOST = 'proxy-server.scraperapi.com'  # rotating proxy or host
PROXY_PORT = 8081 # port
PROXY_USER = 'scraperapi' # username
PROXY_PASS = '2348599934a91db3ea96d44db5d8904a' # password

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (
    PROXY_HOST,
    PROXY_PORT,
    PROXY_USER,
    PROXY_PASS,
)

pluginfile = "proxy_auth_plugin.zip"


def get_chromedriver(use_proxy=True, user_agent=None):
    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = uc.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

    with zipfile.ZipFile(pluginfile, "w") as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    chrome_options = uc.ChromeOptions()
    chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = uc.Chrome(options=chrome_options)
    return driver

def main():
    driver = get_chromedriver(use_proxy=True)
    #driver.get('https://www.google.com/search?q=my+ip+address')
    #driver.get('https://httpbin.org/ip')
    driver.get('https://ipleak.net')
    time.sleep(5)

if __name__ == '__main__':

    main()