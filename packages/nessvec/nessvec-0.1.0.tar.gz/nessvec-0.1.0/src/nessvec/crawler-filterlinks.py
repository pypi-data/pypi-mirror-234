import requests
resp = requests.get('https://dumps.wikimedia.org/enwiki/latest/')
resp.content
print(resp.content)
print(resp.text)
from bs4 import BeautifulSoup, SoupStrainer

for link in BeautifulSoup(resp, parse_only=SoupStrainer('a')):
    if link.has_attr('href'):
        print(link['href'])
from bs4 import BeautifulSoup, SoupStrainer

for link in BeautifulSoup(resp.text, parse_only=SoupStrainer('a')):
    if link.has_attr('href'):
        print(link['href'])
from bs4 import BeautifulSoup
soup = BeautifulSoup(resp.text):
links = soup.findall('a', href=True)
from bs4 import BeautifulSoup
soup = BeautifulSoup(resp.text)
links = soup.findall('a', href=True)
soup

soup = BeautifulSoup(resp.text)
soup
links = soup.find_all('a', href=True)
links
links[0]
links[0].href
type(links[0])
[l.href for l in links]
dir(l)
dir(links[0])
links[0].hasattr('href')
links[0].hasattr('a')
links[0].hasattr
links[0].name
links[0].text
links = [x.text for x in links]
links
for x in links:
    if re.match(r'enwiki-latest.*-abstract[0-9]{1,3}.xml.gz', x):
        print(x)
import re
for x in links:
    if re.match(r'enwiki-latest.*-abstract[0-9]{1,3}.xml.gz', x):
        print(x)
for x in links:
    if re.match(r'^enwiki-latest.*-abstract[0-9]{1,3}.xml.gz$', x):
        print(x)
pwd
hist >> src/nessvec/crawler.py
hist >> src/nessvec/crawler.py
ls -hal
ls src/nessvec/crawler.py
more src/nessvec/crawler.py
hist -f src/nessvec/crawler-filterlinks.py
