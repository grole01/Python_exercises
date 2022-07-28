import re
import json
import requests
from bs4 import BeautifulSoup


url = "https://pk.profdir.com/jobs-for-angular-developer-lahore-punjab-cddb"
soup = BeautifulSoup(requests.get(url).content, "html5lib")

data = soup.select_one('script[type="application/ld+json"]').contents[0]

# fix "broken" description
data = re.sub(
    r'(?<="description" : )"(.*?)"(?=,\s+")',
    lambda g: json.dumps(g.group(1)),
    data,
    flags=re.S,
)

data = json.loads(data, indent=4)

#print(json.dumps(data, indent=4))
print(data)