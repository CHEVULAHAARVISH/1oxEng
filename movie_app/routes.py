from flask import Flask, jsonify, request
from movie_app import app,db
from movie_app.models import Movie,Actor,Genre,Technician
@app.route('/',methods=['Get'])
def hello_world():
    return "Hi 10xEngg"

#now validating data types wheather are we getting proper data or not 
def validate_movie_data(data):
    if not isinstance(data.get('name'), str) or \
       not isinstance(data.get('year_of_release'), int) or \
       not isinstance(data.get('user_ratings'), float) or \
       not isinstance(data.get('genres'), list) or \
       not isinstance(data.get('actors'), list) or \
       not isinstance(data.get('technicians'), list):
        return {'status': 0, 'error': 'Invalid data types'}, None
    return {'status': 1, 'message': 'Success'}, None
# API to get all movies[GET]
#eg url http://localhost:3000/movies
@app.route('/movies', methods=['GET'])
def get_all_movies():
    try:
        movies = Movie.query.all()
        movie_list = [movie.to_dict() for movie in movies]
        return jsonify({'movies': movie_list})
    except Exception as e:
        return jsonify({'status': 0, 'error': str(e)}), 500

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
    try: 
        # Check if a movie ID is provided in the request or not
        if movie_id is None:
            return jsonify({'status': 0, 'error': 'No movie ID provided in the request'}), 400
        movie = Movie.query.get(movie_id)
        if movie:
            return jsonify({'movie': movie.to_dict(), 'status': 1, 'message': 'Success'})
        return jsonify({'status': 0, 'error': 'Movie not found'}), 404
    except Exception as e:
          # Handle unexpected errors with a generic message
        return jsonify({'status': 0, 'error': str(e)}), 500

'''
Invisible Method
def get_movie_by_id(movie_id):
    movie = Movie.query.get(movie_id)
    if movie and movie.is_visible:
        return jsonify(movie.to_dict())
    return jsonify({'error': 'Movie not found'}), 404'''

    
#api to get movie with multiple or filters
@app.route('/movie', methods=['GET'])
def get_all_moviesbycondi():
    try:
        # Get query parameters from the request
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        actor = request.args.get('actor')
        genre = request.args.get('genre')
        user_rating = request.args.get('user_rating')
        name = request.args.get("name")

        # Build the query based on parameters
        query = Movie.query
        if name:
            query = query.filter(Movie.name == name)
        if genre:
            query = query.filter(Movie.genres.any(name=genre))
        if actor:
            query = query.filter(Movie.actors.any(name=actor))
        if user_rating:
            query = query.filter(Movie.user_ratings == float(user_rating))
         # Paginate the results and convert to a dictionary
        movies = query.paginate(page=page, per_page=per_page)
        movie_list = [movie.to_dict() for movie in movies.items]
        
        return jsonify({
            'movies': movie_list,
            'total_pages': movies.pages,
            'current_page': movies.page,
            'total_movies': movies.total,
            'status': 1,
            'message': 'Success'
        })
    except ValueError as ve:
        # Handle invalid data type errors
        return jsonify({'status': 0, 'error': f'Invalid data: {ve}'}), 400
    except Exception as e:
        # Handle unexpected errors with a generic message
        return jsonify({'status': 0, 'error': str(e)}), 500

# api to add a new movie[POST]
@app.route('/movies', methods=['POST'])
def create_movie():
    try: 
        # Get JSON data from the request
        data = request.get_json()
         # Check if data is provided
        if not data:
            return jsonify({'status': 0, 'error': 'No data provided in the request'}), 400

        # Validate data types
        validation_result, _ = validate_movie_data(data)

        if validation_result['status'] == 0:
            return jsonify(validation_result), 400

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
        # Check if the movie already exists
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

        # Add the movie to the database
        db.session.add(new_movie)
        db.session.commit()

        return jsonify({'message': 'Movie created successfully'}), 201
    except ValueError as ve:
        # Handle invalid data errors
        return jsonify({'status': 0, 'error': f'Invalid data: {ve}'}), 400

    except Exception as e:
         # Handle unexpected errors with a generic message
        return jsonify({'status': 0, 'error': str(e)}), 500
    
#api for updating movie with movie name did name for convience[PATCH]
@app.route('/movies/<string:movie_name>', methods=['PATCH'])
def update_movie(movie_name):
    try:
        movie = Movie.query.filter_by(name=movie_name).first()
        if movie:
            # Check if data is provided
            data = request.get_json()
            if not data:
                return jsonify({'status': 0, 'error': 'No data provided in the request'}), 400

            # Validate data types
            validation_result, _ = validate_movie_data(data)
            if validation_result['status'] == 0:
                return jsonify(validation_result), 400

            # Update movie attributes
            movie.name = data.get('name', movie.name)
            movie.year_of_release = data.get('year_of_release', movie.year_of_release)
            movie.user_ratings = data.get('user_ratings', movie.user_ratings)

            # Update genres
            genres_data = data.get('genres', [])
            movie.genres = [Genre(name=genre) for genre in genres_data]

            # Update actors
            actors_data = data.get('actors', [])
            movie.actors = [Actor(name=actor) for actor in actors_data]

            # Update technicians
            technicians_data = data.get('technicians', [])
            movie.technicians = [Technician(name=technician) for technician in technicians_data]

            # Commit changes to the database
            db.session.commit()
            
            return jsonify({'message': 'Movie updated successfully'})
        return jsonify({'error': 'Movie not found'}), 404
    except ValueError as ve:
        # Handle invalid data errors
        return jsonify({'status': 0, 'error': f'Invalid data: {ve}'}), 400
    except Exception as e:
        # Handle unexpected errors with a generic message
        return jsonify({'status': 0, 'error': str(e)}), 500

#api route to delete all movies in data base
@app.route('/movies', methods=['DELETE'])
def delete_all_movies():
    try:   
        # Get all movies and delete them from the database
        movies = Movie.query.all()
        for movie in movies:
            db.session.delete(movie)
        db.session.commit()
        return jsonify({'message': 'All movies deleted successfully'})
    except Exception as e:
          # Handle unexpected errors with a generic message
        return jsonify({'status': 0, 'error': str(e)}), 500
    
#api route to delte movie with id
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    try:
         # Find the movie by its ID
        movie = Movie.query.get(movie_id)
        if movie:
            # Check if the actor is not associated with any other movies
            actors_to_delete = [actor for actor in movie.actors if len(actor.movies) == 1]
            for actor in actors_to_delete:
                db.session.delete(actor)

            # Delete the movie and commit changes        
            db.session.delete(movie)
            db.session.commit()
            return jsonify({'status': 1, 'message': 'Movie deleted successfully'})
        return jsonify({'status': 0, 'error': 'Movie not found'}), 404  
    except Exception as e:
         # Handle unexpected errors with a generic message
        return jsonify({'status': 0, 'error': str(e)}), 500

'''def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        movie.is_visible = False
        db.session.commit()
        return jsonify({'message': 'Movie deleted successfully'})
    return jsonify({'error': 'Movie not found'}), 404
'''
#delete the actor if he is not associated in any movies
@app.route('/actors/<string:actor_name>', methods=['DELETE'])
def delete_actor(actor_name):
    try:
        # Find the actor by their name
        actor = Actor.query.filter_by(name=actor_name).first()
        if actor:
            # Check if the actor is not associated with any movies
            if not actor.movies:
                 # Delete the actor and commit changes
                db.session.delete(actor)
                db.session.commit()
                return jsonify({'status': 1, 'message': 'Actor deleted successfully'})
            else:
                 # Provide an error message if the actor is associated with movies
                movie_list = [movie.to_dict() for movie in actor.movies]
                return jsonify({'status': 0, 'error': 'Actor is associated with movies', 'movies': movie_list}), 400
        return jsonify({'status': 0, 'error': 'Actor not found'}), 404
    except Exception as e:
          # Handle unexpected errors with a generic message
        return jsonify({'status': 0, 'error': str(e)}), 500

'''Invisible Method
def delete_actor(actor_id):
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

'''Mentioned Alternate methods to make data disabled instead of deleting from db since it is bad practice'''