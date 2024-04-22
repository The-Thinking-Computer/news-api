from flask import Flask
from .article_controller import article_routes
from .user_controller import user_routes
from .source_controller import source_routes

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(article_routes, url_prefix='/api/articles')
    app.register_blueprint(user_routes, url_prefix='/api/users')
    app.register_blueprint(source_routes, url_prefix='/api/sources')

    return app