from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json

def get_formatted_datetime():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted_datetime
def get_parent_url(link):
    try:
        parsed_url = urlparse(link)
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc
        parent_url = f"{scheme}://{netloc}/"

        return parent_url

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def get_links(url):
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'lxml')

    links = []
    for link in soup.find_all('a'):
        link_url = link.get('href')

        if link_url is not None and link_url.startswith('http'):
            if "wnep" in link_url:
                if "article" in link_url:            
                    links.append(link_url + '\n')
            if "pennsnortheast" in link_url:
                if "article" in link_url:
                    links.append(link_url + '\n')
            if "pahomepage" in link_url:
                if "news" in link_url:
                    links.append(link_url + '\n')
    return links

def write_articles_to_json(data):
        with open(f'../app/data/data__{str(get_formatted_datetime())}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)