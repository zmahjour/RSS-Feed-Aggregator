import xml.etree.ElementTree as ET
import requests
from datetime import datetime

from podcasts.models import Category, Channel, Episode


def get_rss_text(rss_url):
    response = requests.get(rss_url)
    rss_text = response.text
    return rss_text


