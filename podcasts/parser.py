from django.forms.models import model_to_dict
import xml.etree.ElementTree as ET
import requests
from datetime import datetime
from podcasts.models import Category, Channel, Episode, Rss


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
        guid = item.find("guid").text.strip()
        if Episode.objects.filter(guid=guid).exists():
            break

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
        return datetime.strptime(datetime_str, datetime_format)
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


def create_channel_dict(channel_data, channel_data_attrs):
    namespace = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"

    try:
        image_url = channel_data_attrs.get(f"{namespace}image").get("href")
    except:
        image_url = None

    channel_dict = {
        "title": channel_data.get("title"),
        "subtitle": channel_data.get(f"{namespace}subtitle"),
        "description": channel_data.get("description"),
        "author": channel_data.get(f"{namespace}author"),
        "pub_date": convert_str_to_datetime(channel_data.get("pubDate")),
        "language": channel_data.get("language"),
        "owner_name": channel_data.get(f"{namespace}name"),
        "owner_email": channel_data.get(f"{namespace}email"),
        "image_url": image_url,
    }

    return channel_dict


def convert_explicit_to_boolean(explicit_value):
    if explicit_value == "yes":
        return True
    elif explicit_value == "no":
        return False
    else:
        return False


def create_episodes_dict_list(items_data, items_data_attrs):
    namespace = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"

    episodes_dict_list = []

    for item_data, item_data_attrs in zip(items_data, items_data_attrs):
        try:
            image_url = item_data_attrs.get(f"{namespace}image").get("href")
        except:
            image_url = None

        episode_dict = {
            "guid": item_data.get("guid"),
            "title": item_data.get("title"),
            "subtitle": item_data.get(f"{namespace}subtitle"),
            "description": item_data.get("description"),
            "author": item_data.get("author"),
            "pub_date": convert_str_to_datetime(item_data.get("pubDate")),
            "duration": item_data.get(f"{namespace}duration"),
            "explicit": convert_explicit_to_boolean(
                item_data.get(f"{namespace}explicit")
            ),
            "episode_type": item_data.get(f"{namespace}episodeType"),
            "image_url": image_url,
            "audio_url": item_data_attrs.get("enclosure").get("url"),
        }

        episodes_dict_list.append(episode_dict)

    return episodes_dict_list


def create_or_update(rss_url):
    # update channel
    rss = Rss.objects.get(rss_url=rss_url)
    rss_text = get_rss_text(rss_url=rss_url)
    channel_data, channel_data_attrs = get_channel_data(rss_text=rss_text)
    channel_dict = create_channel_dict(
        channel_data=channel_data, channel_data_attrs=channel_data_attrs
    )
    try:
        channel = Channel.objects.get(rss=rss)
        existing_channel_dict = model_to_dict(channel)

        for key in channel_dict:
            if channel_dict[key] != existing_channel_dict[key]:
                setattr(channel, key, channel_dict[key])
    except:
        channel = Channel.objects.create(**channel_dict, rss=rss)

    categories = create_category_list(channel_data_attrs=channel_data_attrs)
    channel.categories.set(categories)
    channel.save()

    # update episodes
    items_data, items_data_attrs = get_items_data(rss_text=rss_text)

    episodes_dict_list = create_episodes_dict_list(
        items_data=items_data, items_data_attrs=items_data_attrs
    )

    episodes = [
        Episode(**episode_dict, channel=channel) for episode_dict in episodes_dict_list
    ]

    Episode.objects.bulk_create(episodes)
