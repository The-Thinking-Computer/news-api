from flask import Flask, render_template
import json
import os
import random
template_dir = os.path.abspath('./templates')
app = Flask(__name__, template_folder=template_dir)

@app.route('/news')
def news():
    # Load JSON data from file
    with open('../data/data__2024-02-21_17-33-44.json', 'r') as file:
        json_data = json.load(file)
    # Render the 'news' template and pass the JSON data to it
    return render_template('news.html', news=json_data)

@app.route('/article/<id>')
def article(id):
    with open('../data/data__2024-02-21_17-33-44.json', 'r') as file:
        json_data = json.load(file)
    for entry in json_data:
        if entry['id']==id:
            article=entry
            break
    return render_template('article.html', item=entry)
