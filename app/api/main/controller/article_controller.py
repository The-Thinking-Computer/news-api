from flask import jsonify, abort
from database import query_db
app.register_blueprint(article_routes, url_prefix='/api/articles')
@article_routes.route('/all', methods=['GET'])
def get_articles():
    articles = query_db('SELECT id, data FROM articles')
    return jsonify(articles)

@article_routes.route('/id/<article_id>', methods=['GET'])
def get_article(article_id):
    article = query_db('SELECT id, data FROM articles WHERE id=?', [article_id], one=True)
    if article is None:
        abort(404)
    return jsonify(article)

@article_routes.route('/date', methods=['GET'])
def get_articles_by_date():
    articles = query_db('SELECT id, data FROM articles ORDER BY date_published DESC')
    return jsonify(articles)

@article_routes.route('/author/<author_name>', methods=['GET'])
def get_articles_by_author(author_name):
    articles = query_db('SELECT id, data FROM articles WHERE author = ?', [author_name])
    return jsonify(articles)

@article_routes.route('/category/<category_name>', methods=['GET'])
def get_articles_by_category(category_name):
    articles = query_db('SELECT id, data FROM articles WHERE category = ?', [category_name])
    return jsonify(articles)

@article_routes.route('/source/<source_name>', methods=['GET'])
def get_articles_by_source(source_name):
    articles = query_db('SELECT id, data FROM articles WHERE source = ?', [source_name])
    return jsonify(articles)