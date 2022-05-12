import json
from bs4 import BeautifulSoup

html = '''
<script type="application/json" data-initial-state="review-filter">
{"languages":[{"isoCode":"all","displayName":"Toutes les langues","reviewCount":"573"},{"isoCode":"fr","displayName":"français","reviewCount":"567"},{"isoCode":"en","displayName":"English","reviewCount":"6"}],"selectedLanguages":["all"],"selectedStars":null,"selectedLocationId":null}
</script>
'''

soup = BeautifulSoup(html, 'html.parser')
res = soup.find('script')
json_object = json.loads(res.contents[0])

for language in json_object['languages']:
    print('{}: {}'.format(language['displayName'], language['reviewCount']))
#output:
