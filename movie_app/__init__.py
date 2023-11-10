from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_DATABASE_URI'] = ''


db = SQLAlchemy(app)
migrate = Migrate(app,db)
from movie_app import routes
