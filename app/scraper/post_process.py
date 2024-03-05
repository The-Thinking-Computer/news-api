import json
from bs4 import BeautifulSoup
def load_json(filename):
    with open(filename) as f:
        return json.load(f)
def load_matching_data(path_to_file, parameter, value):
    raw_data=load_json(path_to_file)
    _new_data=[]
    for entry in raw_data:
        if(entry['parameter']==value):
            _new_data.append(entry)
    return _new_data
def clean_data(entry):
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