from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://haoounrilwyzlx:5e6b5a73db90a7a817e0177a0d4772c5898e6faab6af0d56854f52e7d39db79a@ec2-52-1-92-133.compute-1.amazonaws.com:5432/d49nsvu08hr5ea' 
db = SQLAlchemy(app)
migrate = Migrate(app,db)
from movie_app import routes