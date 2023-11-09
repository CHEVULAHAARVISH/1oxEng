from flask import Flask, jsonify, request
from movie_app import app,db
from movie_app.models import Movie,Actor,Genre,Technician
@app.route('/',methods=['Get'])
def hello_world():
    return "Hi 10xEngg"

# API to get all movies[GET]
#eg url http://localhost:3000/movies
@app.route('/movies', methods=['GET'])
def get_all_movies():
    movies = Movie.query.all()
    movie_list = [movie.to_dict() for movie in movies]
    return jsonify({'movies': movie_list})

''' 
Invisible method
def get_all_movies():
        movies = Movie.query.filter_by(is_visible=True).all()
        movie_list = [movie.to_dict() for movie in movies]
        return jsonify({'movies': movie_list})
'''
#api to movies by its id[GET]
#eg url http://localhost:3000/movies/1
@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        return jsonify(movie.to_dict())
    return jsonify({'error': 'Movie not found'}), 404

'''
Invisible Method
def get_movie_by_id(movie_id):
    movie = Movie.query.get(movie_id)
    if movie and movie.is_visible:
        return jsonify(movie.to_dict())
    return jsonify({'error': 'Movie not found'}), 404'''
#delete the actor if he is not associated in any movies
@app.route('/actors/<string:actor_name>', methods=['DELETE'])
def delete_actor(actor_name):
    actor = Actor.query.filter_by(name=actor_name).first()
    if actor:
        if not actor.movies:
            db.session.delete(actor)
            db.session.commit()
            return jsonify({'message': 'Actor deleted successfully'})
        else:
            movie_list = [movie.to_dict() for movie in actor.movies]
            return jsonify({'error': 'Actor is associated with movies', 'movies': movie_list}), 400
    return jsonify({'error': 'Actor not found'}), 404


'''def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor:
        visible_movies = [movie for movie in actor.movies if movie.is_visible]
        if not visible_movies:
            actor.is_visible = False
            db.session.commit()
            return jsonify({'message': 'Actor made invisible successfully'})
        else:
            movie_list = [movie.to_dict() for movie in visible_movies]
            return jsonify({'error': 'Actor is associated with visible movies', 'movies': movie_list}), 400
    return jsonify({'error': 'Actor not found'}), 404
'''
# api to add a new movie[POST]
@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    # Get the genre, actor, and technician data from the JSON
    genres_data = data.get('genres', [])
    actors_data = data.get('actors', [])
    technicians_data = data.get('technicians', [])
    # Create Movie instance
    new_movie = Movie(
        name=data['name'],
        year_of_release=data['year_of_release'],
        user_ratings=data['user_ratings']
    )
    existing_movie = Movie.query.filter_by(name=new_movie.name, year_of_release=new_movie.year_of_release).first()
    if existing_movie:
        return jsonify({'error': 'Movie already exists'}), 400

    # Create Genre instances and assign them to the movie
    genres = [Genre(name=genre) for genre in genres_data]
    new_movie.genres.extend(genres)
    
    # Create Actor instances and assign them to the movie
    actors = [Actor(name=actor) for actor in actors_data]
    new_movie.actors.extend(actors)
    
    # Create Technician instances and assign them to the movie
    technicians = [Technician(name=technician) for technician in technicians_data]
    new_movie.technicians.extend(technicians)
    
    db.session.add(new_movie)
    db.session.commit()
    
    return jsonify({'message': 'Movie created successfully'}), 201


#api for updating movie with movie name did name for convience[PATCH]
@app.route('/movies/<string:movie_name>', methods=['PATCH'])
def update_movie(movie_name):
    movie = Movie.query.filter_by(name=movie_name).first()
    
    if movie:
        data = request.get_json()
        movie.name = data.get('name', movie.name)
        movie.year_of_release = data.get('year_of_release', movie.year_of_release)
        movie.user_ratings = data.get('user_ratings', movie.user_ratings)
        
        genres_data = data.get('genres', [])
        genres = [Genre(name=genre) for genre in genres_data]
        movie.genres = genres
        
        actors_data = data.get('actors', [])
        actors = [Actor(name=actor) for actor in actors_data]
        movie.actors = actors
        
        technicians_data = data.get('technicians', [])
        technicians = [Technician(name=technician) for technician in technicians_data]
        movie.technicians = technicians
        
        db.session.commit()
        
        return jsonify({'message': 'Movie updated successfully'})
    
    return jsonify({'error': 'Movie not found'}), 404

#api to get movie with multiple or filters
@app.route('/movie', methods=['GET'])
def get_all_moviesbycondi():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    actor = request.args.get('actor')
    genre = request.args.get('genre')
    user_rating = request.args.get('user_rating')
    name=request.args.get("name")
    
    query = Movie.query
    if name:
        query = query.filter(Movie.name == name)
    if genre:
        query = query.filter(Movie.genres.any(name=genre))
    if actor:
        query = query.filter(Movie.actors.any(name=actor))
    if user_rating:
        query = query.filter(Movie.user_ratings == float(user_rating))
    
    movies = query.paginate(page=page, per_page=per_page)
    movie_list = [movie.to_dict() for movie in movies.items]
    
    return jsonify({
        'movies': movie_list,
        'total_pages': movies.pages,
        'current_page': movies.page,
        'total_movies': movies.total
    })
@app.route('/movies', methods=['DELETE'])
def delete_all_movies():
    movies = Movie.query.all()
    for movie in movies:
        db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'All movies deleted successfully'})

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return jsonify({'message': 'Movie deleted successfully'})
    return jsonify({'error': 'Movie not found'}), 404

'''def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        movie.is_visible = False
        db.session.commit()
        return jsonify({'message': 'Movie deleted successfully'})
    return jsonify({'error': 'Movie not found'}), 404
'''

'''Mentioned Alternate methods to make data disabled instead of deleting from db since it is bad practice'''