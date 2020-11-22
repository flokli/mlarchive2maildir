import requests
from bs4 import BeautifulSoup


def get_mbox_urls(url):
    """parses a pipermail archive list, yields the urls to its archives"""
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for link in soup.find_all('a'):
        if 'Text' in link.text:
            href = link.get('href')
            if href.endswith('.txt') or href.endswith('.txt.gz'):
                yield '{}/{}'.format(url, link.get('href'))
