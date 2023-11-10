# movie_app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # Configurations and other setup can be added here

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://movie_app_9quc_user:wBqAtkECtDgcwguKSSKIVUZOJwhNJMhP@dpg-cl70smoicrhc73cvl3ng-a.oregon-postgres.render.com/movie_app_9quc'
    
    db.init_app(app)
    migrate.init_app(app, db)

    from movie_app import routes

    return app
