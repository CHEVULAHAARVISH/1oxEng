from movie_app import db

# Movie model representing a movie in our database
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Movie name
    year_of_release = db.Column(db.Integer)  # Release year
    user_ratings = db.Column(db.Float)  # User ratings
    genres = db.relationship('Genre', secondary='movie_genre', backref='movies')  # Genres associated with the movie
    actors = db.relationship('Actor', secondary='movie_actor', backref='movies')  # Actors in the movie
    technicians = db.relationship('Technician', secondary='movie_technician', backref='movies')  # Technicians involved
    is_visible = db.Column(db.Boolean, default=True)  # Flag to mark if the movie is visible

    def to_dict(self):
        # Convert Movie object to a dictionary for easy use in APIs
        return {
            'id': self.id,
            'name': self.name,
            'year_of_release': self.year_of_release,
            'user_ratings': self.user_ratings,
            'genres': [genre.name for genre in self.genres],
            'actors': [actor.name for actor in self.actors],
            'technicians': [technician.name for technician in self.technicians],
            'is_visible': self.is_visible
        }

# Genre model representing different movie genres
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # Genre name

# Table to associate movies with genres in a many-to-many relationship
movie_genre = db.Table('movie_genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)

# Actor model representing actors in movies
class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)  # Actor name

# Table to associate movies with actors in a many-to-many relationship
movie_actor = db.Table('movie_actor',
    db.Column('movie_id', db.Integer, db.ForeignKey("movie.id")),
    db.Column('actor_id', db.Integer, db.ForeignKey("actor.id"))
)

# Technician model representing technicians involved in movies
class Technician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)  # Technician name

# Table to associate movies with technicians in a many-to-many relationship
movie_technician = db.Table('movie_technician',
    db.Column('movie_id', db.Integer, db.ForeignKey("movie.id")),
    db.Column('technician_id', db.Integer, db.ForeignKey("technician.id"))
)
