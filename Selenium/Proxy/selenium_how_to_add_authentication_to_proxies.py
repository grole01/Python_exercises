from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time


# replace 'user:pass@ip:port' with your information
API_KEY = '2348599934a91db3ea96d44db5d8904a'

seleniumwire_options = {
            'proxy': {
                'http': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
                'https': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
                'no_proxy': 'localhost,127.0.0.1'
            }
        }

# replace 'your_absolute_path' with your chrome binary's aboslute path
driver = webdriver.Chrome(ChromeDriverManager().install(), seleniumwire_options=seleniumwire_options)

driver.get('http://whatismyipaddress.com')

time.sleep(8)

driver.quit()