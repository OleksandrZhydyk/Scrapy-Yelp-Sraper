import os
from urllib.parse import urlencode


SCRAPEOPS_API_KEY = os.getenv('SCRAPEOPS_API_KEY')


def get_proxy_url(url):
    payload = {"api_key": SCRAPEOPS_API_KEY, "url": url}
    return "https://proxy.scrapeops.io/v1/?" + urlencode(payload)
