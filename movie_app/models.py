
from movie_app import db
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year_of_release = db.Column(db.Integer)
    user_ratings = db.Column(db.Float)
    genres = db.relationship('Genre', secondary='movie_genre', backref='movies')
    actors = db.relationship('Actor', secondary='movie_actor', backref='movies')
    technicians = db.relationship('Technician', secondary='movie_technician', backref='movies')
    is_visible = db.Column(db.Boolean, default=True) # this variable helps us in making it invisible instead of deleting
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'year_of_release': self.year_of_release,
            'user_ratings': self.user_ratings,
            'genres': [genre.name for genre in self.genres],
            'actors': [actor.name for actor in self.actors],
            'technicians': [technician.name for technician in self.technicians],
            'is_visible':self.is_visible

        }

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

movie_genre = db.Table('movie_genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)
class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(),nullable=False)

movie_actor = db.Table('movie_actor',
    db.Column('movie_id', db.Integer, db.ForeignKey("movie.id")),
    db.Column('actor_id', db.Integer, db.ForeignKey("actor.id"))
)
class Technician(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(),nullable=False)

movie_technician = db.Table('movie_technician',
    db.Column('movie_id', db.Integer, db.ForeignKey("movie.id")),
    db.Column('technician_id', db.Integer, db.ForeignKey("technician.id")))
