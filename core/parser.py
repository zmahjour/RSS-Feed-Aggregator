import xml.etree.ElementTree as ET
import requests
from datetime import datetime

from podcasts.models import Category, Channel, Episode


def get_rss_text(rss_url):
    response = requests.get(rss_url)
    rss_text = response.text
    return rss_text


def get_channel_data(rss_text):
    root = ET.fromstring(rss_text)
    channel_data = {}
    channel_data_attrs = {}
    categories = "{http://www.itunes.com/dtds/podcast-1.0.dtd}category"
    channel_data_attrs[categories] = []

    for element in root.find("channel").iter():
        element_text = None
        if element.tag == "item":
            break

        if element.tag != "channel":
            if element.text:
                element_text = element.text.strip()
            channel_data[element.tag] = element_text

            if element.attrib:
                if element.tag == categories:
                    category = element.attrib.get("text")
                    channel_data_attrs[categories].append(category)
                else:
                    channel_data_attrs[element.tag] = element.attrib

    return channel_data, channel_data_attrs

