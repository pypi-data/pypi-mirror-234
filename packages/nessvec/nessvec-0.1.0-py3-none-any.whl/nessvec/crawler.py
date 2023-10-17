import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
import gzip
from tqdm import tqdm


def filter_word_lines(
    pattern=r'^[a-zA-Z_]+[-a-zA-Z_]*$',
    filename='enwiktionary-20210320-all-titles-in-ns0',
    numlines=6637108
):
    pattern = re.compile(pattern)
    cleaned_filename = filename + '.cleaned'
    with Path(filename).open() as fin:
        with Path(cleaned_filename).open('wt') as fout:
            for i, word in enumerate(tqdm(fin, total=numlines)):
                # print(word)
                if pattern.match(word):
                    if not (i % 1000000):
                        print(i, word)
                    fout.writelines([word])
    return cleaned_filename


def make_absolute_url(url, parent):
    if parent in url or url.startswith('http'):
        return url
    return parent.rstrip('/') + '/' + url


def download_wikipedia_abstracts(
    url='https://dumps.wikimedia.org/enwiki/latest/',
    pattern=r'^enwiki-latest.*-abstract[0-9]{1,3}.xml.gz$',
    outpath='enwiki-latest-abstracts.xml'
):
    outpath = Path(outpath)
    links = find_links(url=url, pattern=pattern)
    text = ''
    for link in tqdm(links):
        link = make_absolute_url(link, url)
        path = download_file(link)
        if Path(path).suffix.lower() == '.gz':
            fin = gzip.open(path, 'rb')
        else:
            fin = open(path, 'rb')
        text += fin.read().decode() + '\n'
    with outpath.open('wt') as fout:
        fout.write(text)
    return outpath


def find_links(url, pattern=None):
    """ Extract all <a href='...'> values from the URL provided

    >>> find_links('https://dumps.wikimedia.org/enwiki/latest/',
    ...     pattern=r'^enwiki-latest.*-abstract[0-9]{1,3}.xml.gz$')
    """
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text)
    links = soup.find_all('a', href=True)
    links = [x.text for x in links]
    if pattern:
        links = [x for x in links if re.match(pattern, x)]
    return links


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    return local_filename
