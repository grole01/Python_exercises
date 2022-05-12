import time
import random
from typing import Any, Union
import undetected_chromedriver.v2 as uc
import os
import zipfile
import time
from time import sleep

host = '107.23.19.8'
port = 3135
username = 'ggwp'
password = 'ggwp123'
'''
host = 'proxy-server.scraperapi.com'
port = 8081
username = 'scraperapi'
password = '2348599934a91db3ea96d44db5d8904a'
'''
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
""" % (host, port, username, password)
pluginfile = "proxy_auth_plugin.zip"

def get_chromedriver(use_proxy=True, user_agent=None):
    #opts = uc.ChromeOptions()
    #opts.add_argument(proxySetting.GetProxyText())
    #driver = uc.Chrome(options=opts)

    path = os.path.dirname(os.path.abspath(__file__))
    chrome_options = uc.ChromeOptions()
    if use_proxy:
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
    if user_agent:
        chrome_options.add_argument('--user-agent=%s' % user_agent)
    driver = uc.Chrome(options=chrome_options)
    return driver


def main():
    driver = get_chromedriver(use_proxy=True)
    # driver.get('https://www.google.com/search?q=my+ip+address')
    driver.get('http://whatismyipaddress.com')
    time.sleep(5)


if __name__ == '__main__':
    main()