import time
from bs4 import BeautifulSoup
import json
import urllib
from urllib.request import urlopen
from xml.etree import ElementTree as ET

def feed_handler(url):
    r=download_xml(url)
    soup=BeautifulSoup
    channels=getchannels(soup);items=getitems(soup)
    data={
        "feed":channels,
        "items":items
    }
    data=json.dumps_data
    with open('rss.json') as output:
        output.write(data)

def get_channels(content):
    channels=[]
    try:
        result=content.find_all('channel')
        for i in result:
            title=i.find('title').text.strip()
            description=i.find('description').text.strip()
            link=i.find('link').text.strip()
            url=i.find('atom:link').text.strip()
            generator=i.find('generator').text.strip()
            image=i.find_all('image')
            for j in image:
                img=j.find('url').text.strip()
            
            data={
                "url":url,
                "title":title,
                "description":description,
                "link":link,
                "image":img,
                "generator":generator,

            }
            channels.append(data)
        channels=json.dumps(channels)
        data=json.loads(channels)
        return data
    except Exception as e:
        return e.__doc__

def get_items(content):
    items=[]
    try:
        result=content.find_all('item')
        for i in result:
            title=i.find('title').text.strip()
            published=i.find('pubDate').text.strip()
            link=i.find('link').text.strip()
            author=i.find('dc:creator').text.strip()
            description=i.find('description').text.strip()
            thumbnail=BeautifulSoup(description, features='xml').select_one('img')[src]

            category=i.find_all('category')
            categories=[]
            for j in category:
                cg=j.text.strip()
                categories.append(cg)

            guid=i.find('guid').text.strip()
            data={
                'title':title,
                'author':author
,               'description':description,
                'thumbnail':thumbnail,
                'link':link,
                'published':published,
                'categories':categories,
                'guid':guid
            }
            items.append(data)
        items=json.dumps(items)
        data=json.loads(items)
        return(data)
    except Exception as e:
        return e.__doc__

def download_xml(url):
    with urllib.request.urlopen(url) as response:
        xml_data = response.read()
    return xml_data

def write_to_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)
