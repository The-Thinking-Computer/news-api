
from gensim import corpora, models
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models import LdaModel
from gensim.test.utils import datapath
import re
import json



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

def pre_pre_pre_process(object,_list):
    id=object['id']
    article_content=(object['content'])['article_content']
    _list.append({"id":id,"data":article_content,"category":None})
    
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

def preprocess_text(text):
    updated_stopwords = STOPWORDS.union(custom_stopwords)
    text = re.sub(r'<.*?>', '', text)  
    tokens = simple_preprocess(text, deacc=True) 
    tokens = [token for token in tokens if token not in updated_stopwords]  
    return tokens

processed_texts = [preprocess_text(article['data']) for article in data]
def get_topics(processed_texts):
    dictionary = corpora.Dictionary(processed_texts)
    corpus = [dictionary.doc2bow(text) for text in processed_texts]
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, passes=20,alpha=0.3,eta=0.95)

    return {"topics": lda_model.show_topics(formatted=False),
            "top_words": [(topic_idx, [word[0] for word in lda_model.show_topic(topic_idx)]) for topic_idx in range(lda_model.num_topics)]
            }
def print_topics(top_words_per_topic):
    topic, words in top_words_per_topic:
    print(f"Topic {topic}: {words}")
predefined_topics={}
for topic, words in top_words_per_topic:
    word_list = [word for word in words]
    predefined_topics[topic] = word_list

def calculate_similarity(document_words, topic_words):
    common_words = set(document_words).intersection(set(topic_words))
    similarity = len(common_words) / max(len(document_words), len(topic_words))
    return similarity

def categorize_data(data)
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

