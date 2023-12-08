import os
import sys
import cloudscraper
import requests

from requests import ConnectTimeout
from bs4 import BeautifulSoup


class NotFoundError(Exception):
    pass


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15'
}
PATH = os.getcwd()


def url_encode(txt):
    '''Encodes txt for url generation'''
    import urllib.parse
    return urllib.parse.quote(txt.encode('utf8'))


def request_base_html(url: str, s: requests.Session) -> BeautifulSoup:
    '''returns html content of requested url'''
    res = request_data(url=url, session=s).content
    html = BeautifulSoup(res, 'html.parser')

    return html


def request_data(url: str, session: requests.Session) -> dict:
    '''performs GET request to given url with given session'''
    try:
        response = session.get(
            timeout=5,
            url=url,
            headers=HEADERS
        )
        return response

    except ConnectTimeout:
        print("Connection Timeout Error")
        sys.exit()


def post_request(post_url: str, post_data: dict):
    session = cloudscraper.CloudScraper()
    session.headers = HEADERS
    response = session.post(
        url=post_url,
        data=post_data,
    )

    return response.content
