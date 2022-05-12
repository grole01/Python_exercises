from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time

# change 'ip:port' with your proxy's ip and port
#proxy_ip_port = 'ip:port'
proxy_ip_port = '8.214.41.50:80'

proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = proxy_ip_port
proxy.ssl_proxy = proxy_ip_port

capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)

# replace 'your_absolute_path' with your chrome binary absolute path
#driver = webdriver.Chrome('your_absolute_path', desired_capabilities=capabilities)
driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=capabilities)


driver.get('http://whatismyipaddress.com')

time.sleep(8)

driver.quit()