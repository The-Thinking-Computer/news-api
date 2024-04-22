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
    """
    Extract the parent URL from a given link.

    This function extracts the parent URL from a given link by parsing the link using the urlparse function from the urllib.parse module. It retrieves the scheme and netloc components of the parsed URL and constructs the parent URL using the scheme and netloc. The parent URL represents the base URL of the website containing the provided link.

    Args:
    - link (str): The URL from which the parent URL will be extracted.

    Returns:
    - str or None: The parent URL extracted from the given link. If an error occurs during parsing, it prints the exception and returns None.
    """
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
    """
    Extract hyperlinks from a webpage URL.

    This function sends an HTTP GET request to the specified URL to retrieve the webpage content. It then parses the HTML content using BeautifulSoup to extract all hyperlink elements ('a' tags) from the webpage. For each hyperlink, it retrieves the URL using the 'href' attribute. If the URL is not None and starts with 'http', it checks if it contains keywords associated with specific news websites ('wnep', 'pennsnortheast', 'pahomepage') and if it includes the term 'article'. If both conditions are met, the URL is appended to a list of links.

    Args:
    - url (str): The URL of the webpage from which hyperlinks will be extracted.

    Returns:
    - list: A list of hyperlinks (URLs) extracted from the webpage that meet the specified criteria.
    """
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
    """
    Write articles data to a JSON file.

    This function writes articles data to a JSON file. It takes a dictionary or list containing articles data as input and dumps it into a JSON file. The filename is generated based on the current date and time using the 'get_formatted_datetime' function.

    Args:
    - data (dict or list): The articles data to be written to the JSON file.

    Returns:
    None
    """
        with open(f'../app/data/data__{str(get_formatted_datetime())}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)