
from gensim import corpora, models
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models import LdaModel
from gensim.test.utils import datapath
import re
import json



custom_stopwords={'said','day','11','news', 'wednesday','stated','tag','city','state','items',"barre","available","worth","new","says","states","county"}
def delete_duplicates(data):
     """
    Delete duplicate items from a list based on a specific data attribute.

    This function takes a list of items, each represented as a dictionary or object, and removes duplicates based on a specific data attribute. It iterates through the list, keeping track of seen data values using a set. If a data value is encountered for the first time, the item is added to a list of unique items; otherwise, it is skipped as a duplicate. The function returns the list of unique items.

    Args:
    - data (list): A list of dictionaries or objects representing items, each containing a 'data' attribute.

    Returns:
    - list: A list of unique items, where duplicates based on the 'data' attribute have been removed.
    """
    seen = set()
    unique_items = []
    
    for item in data:
        data_value = item["data"] if isinstance(item, dict) else getattr(item, "data")
        
        if data_value not in seen:
            seen.add(data_value)
            unique_items.append(item)
    
    return unique_items

def pre_pre_pre_process(object,_list):
    """
    Perform preliminary (pre-pre)preprocessing of article content.

    This function extracts the ID and article content from the provided object dictionary,
    appends the extracted data to the given list with an initially None category.

    Args:
    - object (dict): A dictionary containing article information, including an ID and content.
    - _list (list): A list to which the processed data will be appended.

    Returns:
    None: Modifies the given list in place by appending a dictionary containing the ID, article content, and initially None category.
    """
    id=object['id']
    article_content=(object['content'])['article_content']
    _list.append({"id":id,"data":article_content,"category":None})
    
def pre_pre_process(data):
    """
    Perform preliminary preprocessing of data before further processing.

    This function performs preliminary preprocessing of data before further processing. If the input data is a list of strings, it assumes each string represents a filename containing JSON data. It then loads each JSON file, iterates through the articles within, and applies a preliminary preprocessing step to each article using the 'pre_pre_pre_process' function.

    If the input data is a string, it assumes it represents a filename containing JSON data. It loads the JSON file, iterates through the articles within, and applies the same preliminary preprocessing step to each article using the 'pre_pre_pre_process' function.

    Args:
    - data (str or list): If a list, each element is treated as a filename containing JSON data. If a string, it is treated as a single filename containing JSON data.

    Returns:
    data (list)
    """
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
                return _data as data
            except:
                continue 
    
#######################FIX THIS######################## 
def preprocess_text(data):
    """
    Preprocess raw text data for natural language processing (NLP) tasks.

    This function preprocesses raw text data for NLP tasks by performing the following steps:
    1. Unionizes the standard STOPWORDS with custom stopwords provided.
    2. Removes HTML tags using regular expressions.
    3. Tokenizes the text into lowercase alphanumeric tokens using the simple_preprocess function from the Gensim library.
    4. Filters out tokens that are stopwords.

    Args:
    - data (str): The raw text data to be preprocessed.

    Returns:
    - list: A list of preprocessed tokens ready for further NLP analysis.
    """
    updated_stopwords = STOPWORDS.union(custom_stopwords)
    text = re.sub(r'<.*?>', '', data)  
    tokens = simple_preprocess(text, deacc=True) 
    tokens = [token for token in tokens if token not in updated_stopwords]  
    return tokens

processed_texts = [preprocess_text(article['pre_pre_process(data)']) for article in data]
def get_topics(processed_texts):
    """
    Generate predefined topics set from a list of top words per topic.

    Args:
    - top_words_per_topic (list): A list of tuples where each tuple contains a topic and its associated top words.

    Returns:
    - dict: A dictionary where keys are topic names and values are sets of top words.
    """
    dictionary = corpora.Dictionary(processed_texts)
    corpus = [dictionary.doc2bow(text) for text in processed_texts]
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, passes=20,alpha=0.3,eta=0.95)

    return {"topics": lda_model.show_topics(formatted=False),
            "top_words": [(topic_idx, [word[0] for word in lda_model.show_topic(topic_idx)]) for topic_idx in range(lda_model.num_topics)]
            }
#################################################

def print_topics(top_words_per_topic):
    topic, words in top_words_per_topic:
    print(f"Topic {topic}: {words}")
predefined_topics={}
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

def categorize_data(data)
    """
    Categorize documents in a dataset based on predefined topics.

    This function categorizes documents in a dataset based on predefined topics. It iterates through each document in the dataset and calculates the similarity between the document's words and each predefined topic using the 'calculate_similarity' function. It assigns the document to the topic with the highest similarity score.

    After categorizing all documents, it updates the 'category' key of each document in the dataset. Additionally, it writes the updated dataset to a JSON file named 'updated_data_file.json' with proper indentation.

    Args:
    - data (list): A list of dictionaries representing documents, where each dictionary contains a 'data' key with text content to be categorized.

    Returns:
    None: Modifies the 'category' key of each document dictionary in place and writes the updated dataset to a JSON file.
    """
    for doc in data:
        document_words = doc["data"].split()  # Split text into words
        
        max_similarity = -1
        assigned_topic = None
        
        # Calculate similarity with each predefined topic
        for topic, topic_words in predefined_topics.items():
            similarity = calculate_similarity(document_words, topic_words)
            if similarity > max_similarity:
                max_similarity = similarity
                assigned_topic = topic
        
        doc["category"] = assigned_topic
    with open("updated_data_file.json", "w") as f:
        json.dump(data, f, indent=4)

