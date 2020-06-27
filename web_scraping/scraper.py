import requests
import re
from urllib.parse import urlparse
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup


def get_valid_link(url):
    url = urlparse(url, 'http').geturl()
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, url):
        return url


def scrape_content(string):
    return BeautifulSoup(string).prettify()


def scrape_url(url, headers=None):
    try:
        page = requests.get(url, headers)
        page.raise_for_status()
    except HTTPError as e:
        print(e)
    except Exception as err:
        print(err)
    else:
        soup = BeautifulSoup(page.content, 'html.parser')
        soup = BeautifulSoup(soup.prettify(), 'html.parser')
        return soup

    return BeautifulSoup("", 'html.parser')
