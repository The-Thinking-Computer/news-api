from bs4.element import Comment
import re
import json
import requests
import urllib.request
from bs4 import BeautifulSoup
import uuid
from time import sleep
import tools
from post_process import clean_data

def PENNS_NORTHEAST_scraper(url):
    """
    Scrape article content from a specific news website.

    This function scrapes article content from a specific news website (PENNS_NORTHEAST) given a URL. It performs the following steps:
    1. Strips leading and trailing whitespace from the URL.
    2. Sends an HTTP GET request to the URL and raises an exception if the response status is not successful.
    3. Parses the HTML content of the response using BeautifulSoup.
    4. Extracts metadata such as title and author from the HTML.
    5. Finds the section containing the article content.
    6. Extracts paragraph elements from the article section.
    7. Concatenates the text content of paragraphs into a single string representing the article content.
    8. Returns a dictionary containing the author, title, and article content.

    Args:
    - url (str): The URL of the webpage containing the article to be scraped.

    Returns:
    - dict or str: A dictionary containing the author, title, and article content if the article is found on the provided URL. If no article is found, it returns the string "No article found on the provided URL.". If an error occurs during scraping, it returns the string "Error fetching article content.".
    """
    try:
        url = url.strip()
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.content, 'html.parser')
        title=soup.find('meta',property="og:title")
        author=soup.find('meta',property="article:publisher")
        title=title['content']
        author=author['content']
        news_post = soup.find('section',_class="news_post")
        abstract=article_tag.get('data-abstract')
        title=article_tag.get('data-title')
        author=article_tag.get('data-author')
        
        if news_post:
            container=news_post.find('div',_class="container")
            rows=container.find_all('div',_class="row")

            paragraph_list=[]

            for row in rows:
                for p in row.find_all('p')
                    paragraph_list.append(p)
            article_str=''
            for q in paragraph_list:
                aticle_str=article_str+str(q)

        ##################################

            return {
                "author":author,
                "title":title,
                "article_content":article_str
                }

        ##################################
        else:
            return "No article found on the provided URL."

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error fetching article content."
def WNEP_scraper(url):
    """
    Scrape article content from WNEP (NewsWatch 16) website.

    This function scrapes article content from the WNEP (NewsWatch 16) website given a URL. It performs the following steps:
    1. Strips leading and trailing whitespace from the URL.
    2. Sends an HTTP GET request to the URL and raises an exception if the response status is not successful.
    3. Parses the HTML content of the response using BeautifulSoup.
    4. Finds the 'article' tag containing the main article content.
    5. Extracts metadata such as title, author, and abstract from the 'article' tag.
    6. Finds the 'div' element with class 'article__body' containing the article body.
    7. Extracts paragraph elements from the article body.
    8. Concatenates the text content of paragraphs into a single string representing the article content.
    9. Returns a dictionary containing the author, title, abstract, and article content.

    Args:
    - url (str): The URL of the webpage containing the article to be scraped.

    Returns:
    - dict or str: A dictionary containing the author, title, abstract, and article content if the article is found on the provided URL. If no article is found, it returns the string "No article tag found on the provided URL.". If an error occurs during scraping, it returns the string "Error fetching article content.".
    """
    try:
        url = url.strip()
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.content, 'html.parser')
        
        article_tag = soup.find('article')
        body = article_tag.find('div', class_="article__body")
        abstract=article_tag.get('data-abstract')
        title=article_tag.get('data-title')
        author=article_tag.get('data-author')
        
        if article_tag:
            article_str=''
            paragraphs = body.find_all('p')
            for paragraph in paragraphs:
                article_str=article_str+str(paragraph)

            return {
                "author":author,
                "title":title,
                "abstract":abstract,
                "article_content":article_str
                }
        else:
            return "No article tag found on the provided URL."

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error fetching article content."
def PAHOMEPAGE_scraper(url):
    """
    Scrape article content from the PAHOMEPAGE website.

    This function scrapes article content from the PAHOMEPAGE website given a URL. It performs the following steps:
    1. Strips leading and trailing whitespace from the URL.
    2. Sends an HTTP GET request to the URL and raises an exception if the response status is not successful.
    3. Parses the HTML content of the response using BeautifulSoup.
    4. Searches for script tags containing the JSON data for the article content.
    5. Extracts metadata such as title, author, and description from the JSON data.
    6. Finds the 'div' element containing the article content.
    7. Extracts paragraph elements from the article content.
    8. Concatenates the text content of paragraphs into a single string representing the article content.
    9. Returns a dictionary containing the title, author, abstract, and article content.

    Args:
    - url (str): The URL of the webpage containing the article to be scraped.

    Returns:
    - dict: A dictionary containing the title, author, abstract, and article content if the article is found on the provided URL. If no article is found, it returns a dictionary with the title, author, description, and 'article_content' set to 'NOT AVAILABLE'. If an error occurs during scraping, it prints the exception and returns an empty dictionary.
    """
    try:
        url = url.strip()
        response = requests.get(url)
        response.raise_for_status()  

        soup = BeautifulSoup(response.content, 'html.parser')
        script_tags = soup.find_all('script')

        matched_line = None
        for script_tag in script_tags:
            if script_tag.string and script_tag.string.strip().startswith('window.NXSTdata = window.NXSTdata || {}'):
                match = re.search(r'window\.NXSTdata\.content\s*=\s*Object\.assign\s*\(\s*window\.NXSTdata\.content\s*,\s*({.*?})\s*\)', script_tag.string)
                if match:
                    matched_line = match.group(0)
                    break

        if matched_line:
            start_index = matched_line.find('{')
            end_index = matched_line.rfind('}') + 1
            content_json = matched_line[start_index:end_index]
            article_data = json.loads(content_json)
            
        if type(article_data)!=None:
            title = article_data.get('title', '')
            author = article_data.get('authorName', '')
            description = article_data.get('description', '')

        div_element = soup.find('div', class_=['article-content', 'article-body', 'rich-text'])
        
        if div_element:
            paragraphs = div_element.find_all('p')
            article_str=''
            for paragraph in paragraphs:
                article_str=article_str+str(paragraph)
            return {
            'title': title,
            'author': author,
            'abstract': description,
            'article_content': article_str
        }
        elif not div_element:
            return {
            'title': title,
            'author': author,
            'description': description,
            'article_content': 'NOT AVAILABLE'
        }
    except Exception as e:
        print(f"EXCEPTION OCCURED: {e}")
all_articles=[]

class Website:
    """
    Represents a website with articles to be scraped.

    This class represents a website with articles to be scraped. It contains methods for recording articles from the website.

    Attributes:
    - name (str): The name of the website.
    - parent_url (str): The base URL of the website.
    - target_url (str): The URL of the specific page containing the articles to be scraped.
    - links (list): A list of links extracted from the target URL.
    - scraper (function): The function used for scraping article content from the website.
    - articles (list): A list to store scraped articles.

    Methods:
    - __init__: Initializes the Website object with the provided attributes.
    - record_articles: Scrapes articles from the website and records them.
    """
    
    def __init__(self, name,parent_url,target_url,scraper,articles=None):
        self.name=name
        self.parent_url:str=parent_url
        self.target_url:str=parent_url+target_url
        self.links:list=tools.get_links(self.target_url)
        self.scraper=scraper
        self.articles=[]
    def record_articles(self):
        print("STARTING RECORD_ARTICLES")
        json_article_list=[]
        for link in self.links:
            if(link==self.target_url):
                continue
            article_json={
                "id": str(uuid.uuid4()),
                "parent_url": tools.get_parent_url(link),
                "link":link,
                "content":(self.scraper(link))
            }
            article_json=clean_data(article_json)
            json_article_list.append(article_json)
        for article in json_article_list:
            print('adding article to all_articles')
            all_articles.append(article)





