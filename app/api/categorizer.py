
from gensim import corpora, models
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models import LdaModel
from gensim.test.utils import datapath
import re
import json


def get_json_files(folder_path):
    """
    Retrieve all JSON files within the specified folder.

    Args:
        folder_path (str): The path to the folder containing the JSON files.

    Returns:
        list: A list of file paths to the JSON files.
    """
    json_files = []
    for file in os.listdir(folder_path):
        if file.endswith('.json'):
            json_files.append(os.path.join(folder_path, file))
    return json_files
data=[]
custom_stopwords={'said','day','11','news', 'wednesday','stated','tag','city','state','items',"barre","available","worth","new","says","states","county"}
def delete_duplicates(data):
    
    seen = set()
    unique_items = []
    
    for item in data:
        data_value = item["data"] if isinstance(item, dict) else getattr(item, "data")
        
        if data_value not in seen:
            seen.add(data_value)
            unique_items.append(item)
    
    return unique_items

def pre_pre_pre_process(object):
    id=object['id']
    article_content=(object['content'])['article_content']
    data.append({"id":id,"data":article_content,"category":None})
    print('added entry to article data')
    
def pre_pre_process(data):
    if type(data)==list:
        for object in data:
            if type(object)==str:
                with open(f"../data/{object}") as file:
                    _data=json.load(file)
                for article in _data:
                    try:
                        pre_pre_pre_process(article)   
                    except:
                        continue

    elif type(data)==str:
        with open(f"../data/{object}") as file:
                    _data=json.load(file)
        for article in _data:
            try:            
                pre_pre_pre_process(DATA)   
            except:
                continue

pre_pre_process(get_json_files('../data'))
data=delete_duplicates(data)

def preprocess_text(text):
    updated_stopwords = STOPWORDS.union(custom_stopwords)
    text = re.sub(r'<.*?>', '', text)  
    tokens = simple_preprocess(text, deacc=True) 
    tokens = [token for token in tokens if token not in updated_stopwords]  
    return tokens

processed_texts = [preprocess_text(article['data']) for article in data]

dictionary = corpora.Dictionary(processed_texts)
corpus = [dictionary.doc2bow(text) for text in processed_texts]
lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, passes=20,alpha=0.3,eta=0.95)

topics = lda_model.show_topics(formatted=False)

top_words_per_topic = [(topic_idx, [word[0] for word in lda_model.show_topic(topic_idx)]) for topic_idx in range(lda_model.num_topics)]


#########################TAKE THIS OUT################
for topic, words in top_words_per_topic:
    print(f"Topic {topic}: {words}")
predefined_topics={}
for topic, words in top_words_per_topic:
    word_list = [word for word in words]
    predefined_topics[topic] = word_list
######################TAKE THIS OUT################

def get_predefined_topics(top_words_per_topic):
    """
    Generate predefined topics set from a list of top words per topic.

    Args:
    - top_words_per_topic (list): A list of tuples where each tuple contains a topic and its associated top words.

    Returns:
    - dict: A dictionary where keys are topic names and values are sets of top words.
    """
    predefined_topics = {}
    for topic, words in top_words_per_topic:
        print(f"Topic {topic}: {words}")
        word_list = [word for word in words]
        predefined_topics[topic] = set(word_list)
    return predefined_topics

def calculate_similarity(document_words, topic_words):
    """
    Calculate the similarity between two lists of words.

    Args:
    - document_words (List[str]): A list of words representing a document.
    - topic_words (List[str]): A list of words representing a topic.

    Returns:
    - float: The similarity between the document and the topic, ranging from 0 to 1.
    """
    common_words = set(document_words).intersection(set(topic_words))
    similarity = len(common_words) / max(len(document_words), len(topic_words))
    return similarity

def assign_category(data, predefined_topics):
    """
    Assigns categories to documents based on predefined topics.

    Args:
    - data (list): A list of dictionaries representing documents.
    - predefined_topics (dict): A dictionary where keys are topic names and values are lists of words representing each topic.

    Returns:
    None: Modifies the 'category' key of each document dictionary in place.
    """
    for doc in data:
        document_words = doc["data"].split()  # Split text into words
        
        max_similarity = -1
        assigned_topic = None
        
        for topic, topic_words in predefined_topics.items():
            similarity = calculate_similarity(document_words, topic_words)
            if similarity > max_similarity:
                max_similarity = similarity
                assigned_topic = topic
        
        doc["category"] = assigned_topic


data= assign_category(data,(predefined_topics.items()))
with open("updated_data_file.json", "w") as f:
    json.dump(data, f, indent=4)
###################################


