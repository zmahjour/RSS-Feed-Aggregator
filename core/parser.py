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


def get_items_data(rss_text):
    root = ET.fromstring(rss_text)
    items_data = []
    items_data_attrs = []
    for item in root.findall(".//item"):
        item_data = {}
        item_data_attrs = {}
        for element in item.iter():
            element_text = None

            if element.tag != "item":
                if element.text:
                    element_text = element.text.strip()
                item_data[element.tag] = element_text

                if element.attrib:
                    item_data_attrs[element.tag] = element.attrib

        items_data.append(item_data)
        items_data_attrs.append(item_data_attrs)

    return items_data, items_data_attrs


def convert_str_to_datetime(datetime_str):
    datetime_format = "%a, %d %b %Y %H:%M:%S %z"
    try:
        datetime.strptime(datetime_str, datetime_format),
    except:
        return None


def create_category_list(channel_data_attrs):
    namespace = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
    categories = channel_data_attrs.get(f"{namespace}category")
    category_list = []
    existing_categories = []
    for category in categories:
        if not Category.objects.filter(title=category).exists():
            category_list.append(Category(title=category))
        else:
            existing_categories.append(Category.objects.get(title=category))
    categories = Category.objects.bulk_create(category_list)
    categories += existing_categories
    return categories


