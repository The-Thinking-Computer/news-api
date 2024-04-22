import json
from bs4 import BeautifulSoup
def load_json(filename):
    with open(filename) as f:
        return json.load(f)
def load_matching_data(path_to_file, parameter, value):
    """
    Load data entries from a JSON file that match a specified parameter and value.

    This function loads data entries from a JSON file located at the given path that match a specified parameter and value. It first loads the JSON file using the 'load_json' function. Then, it iterates through each entry in the loaded data. If an entry has the specified parameter with a value matching the given value, it appends the entry to a new list. Finally, it returns the list of matching data entries.

    Args:
    - path_to_file (str): The file path to the JSON file containing the data entries.
    - parameter (str): The parameter to match against.
    - value (any): The value to match against the specified parameter.

    Returns:
    - list: A list of data entries from the JSON file that match the specified parameter and value.
    """
    raw_data=load_json(path_to_file)
    _new_data=[]
    for entry in raw_data:
        if(entry['parameter']==value):
            _new_data.append(entry)
    return _new_data
def clean_data(entry):
    """
    Clean the content of an entry dictionary representing a web page.

    This function cleans the content of an entry dictionary representing a web page by removing specific elements based on the parent URL. It first checks if the parent URL matches known domains ('https://pahomepage.com' or 'https://wnep.com'). If the parent URL matches 'https://pahomepage.com', it removes all 'aside' elements from the HTML content. If the parent URL matches 'https://wnep.com', it removes specific 'div' elements with classes 'article__section' or 'article__section_type_ad' from the HTML content. After cleaning, it updates the 'article_content' key of the 'content' dictionary within the entry with the modified HTML content.

    Args:
    - entry (dict): A dictionary representing an entry containing web page content, including the parent URL and content HTML.

    Returns:
    - dict: The modified entry dictionary with cleaned content.
    """
    try:
        if entry['parent_url']=="https://pahomepage.com":
            entry_content=(entry['content'])
            entry_content=entry_content['article_content']
            if entry_content=="NOT AVAILABLE":
                pass
            soup = BeautifulSoup(entry_content, 'html.parser')
            for aside in soup.find_all('aside'):
                aside.extract()
            modified_html_content = str(soup)
            (entry['content'])['article_content']=modified_html_content
        elif entry['parent_url']=="https://wnep.com":
            entry_content=(entry['content'])
            entry_content=entry_content['article_content']
            if entry_content=="NOT AVAILABLE":
                pass
            soup = BeautifulSoup(entry_content, 'html.parser')
            for ad_div in soup.find_all('div',class_=['article__section','article__section_type_ad']):
                ad_div.extract()
            modified_html_content=str(soup)
            (entry['content'])['article_content']=modified_html_content
    except Exception as e:
        print(f'EXCEPTION OCCURED {e}')
    return entry