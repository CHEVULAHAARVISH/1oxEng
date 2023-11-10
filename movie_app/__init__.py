from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db' 
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wysxiyjypzwsha:5f1c36fc53f8a75cc88ec5974dfdc5774c85c25ea32a484a16bcefcd8db7e7e8@ec2-44-215-22-37.compute-1.amazonaws.com:5432/de3bolos0fletr'
db = SQLAlchemy(app)
migrate = Migrate(app,db)
from movie_app import routes