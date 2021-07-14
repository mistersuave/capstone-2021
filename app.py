import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor, movie_items
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # ROUTES
    '''
	@TODO implement endpoint
	    GET /actors
		it should be a public endpoint
		it should contain only the actors.format() data representation
		returns status code 200 and json {"success": True, "actors": actors}
		where actors is the list of actors
		or appropriate status code indicating reason for failure
	'''

    @app.route('/actors', methods=['GET'])
    def get_actors():
        return jsonify(
            {
                'success': True,
                'actors': [actor.format() for actor in Actor.query.all()]
            }), 200

    '''
	@TODO implement endpoint
	    GET /actors/<id>
		where <id> is the existing model id
		it should respond with a 404 error if <id> is not found
		it should contain the drink.long() data representation
		returns status code 200 and json {"success": True, "actors": actor}
		where actor is the details of updated actor
		or appropriate status code indicating reason for failure
	'''

    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor_by_id(jwt, actor_id):
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)

        return jsonify(
            {
                'success': True,
                'actor': actor.format()
            }), 200

    '''
	@TODO implement endpoint
	    POST /actors
		it should create a new row in the actors table
		it should require the 'post:actors' permission
		returns status code 200 and json {"success": True, "actor": actor}
		where actor is the id of the newly created actor
		or appropriate status code indicating reason for failure
	'''

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_new_actor(jwt):
        data = json.loads(request.data)
        if 'name' and 'gender' not in data:
            abort(422)

        try:
            actor = Actor(name=data['name'],
                          gender=data['gender'], age=data['age'])
            actor.insert()
            return jsonify(
                {
                    'success': True,
                    'actor': actor.id
                }), 200

        except ex:
            db.session.rollback()
            abort(500)

    '''
	@TODO implement endpoint
	    PATCH /actors/<id>
		where <id> is the existing model id
		it should respond with a 404 error if <id> is not found
		it should contain the drink.long() data representation
		returns status code 200 and json {"success": True, "actors": actor}
		where actor is the details of updated actor
		or appropriate status code indicating reason for failure
	'''

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor_by_id(jwt, actor_id):
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)

        try:
            data = json.loads(request.data)
            if 'name' in data:
                actor.name = data['name']

            if 'age' in data:
                actor.age = data['age']

            if 'gender' in data:
                actor.gender = data['gender']

            actor.update()
            return jsonify(
                {
                    'success': True,
                    'actors': actor.format()
                }), 200

        except ex:
            abort(500)

    '''
	@TODO implement endpoint
	    DELETE /actors/<id>
		where <id> is the existing model id
		it should respond with a 404 error if <id> is not found
		it should delete the corresponding row for <id>
		it should require the 'delete:actors' permission
		returns status code 200 and json {"success": True, "delete": id}
		where id is the id of the deleted record
		or appropriate status code indicating reason for failure
	'''

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)

        try:
            actor.delete()

            return jsonify(
                {
                    'success': True,
                    'delete': actor.id
                }), 200

        except ex:
            db.session.rollback()
            abort(500)

    '''
	@TODO implement endpoint
	    GET /movies
		it should be a public endpoint
		it should contain only the movies.format() data representation
		returns status code 200 and json {"success": True, "movies": movies}
		where movies is the list of movies
		or appropriate status code indicating reason for failure
	'''

    @app.route('/movies', methods=['GET'])
    def get_movies():
        return jsonify(
            {
                'success': True,
                'movies': [movie.format() for movie in Movie.query.all()]
            }), 200

    '''
	@TODO implement endpoint
	    GET /movies/<id>
		where <id> is the existing model id
		it should respond with a 404 error if <id> is not found
		it should contain the drink.long() data representation
		returns status code 200 and json {"success": True, "movies": movie}
		where movie is the details of the queried movie
		or appropriate status code indicating reason for failure
	'''

    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie_by_id(jwt, movie_id):
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)

        return jsonify(
            {
                'success': True,
                'movies': movie.format()
            }), 200

    '''
	@TODO implement endpoint
	    POST /movies
		it should create a new row in the movies table
		it should require the 'post:movies' permission
		returns status code 200 and json {"success": True, "movies": movie}
		where movie is the id of the newly created movie
		or appropriate status code indicating reason for failure
	'''

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_new_movie(jwt):
        data = json.loads(request.data)
        if 'title' and 'date' not in data:
            abort(422)

        try:
            movie = Movie(title=data['title'], date=data['date'])
            movie.insert()
            return jsonify(
                {
                    'success': True,
                    'movie': movie.id
                }), 200

        except ex:
            db.session.rollback()
            abort(500)

    ''' 
	@TODO implement endpoint
	    PATCH /movies/<id>
		where <id> is the existing model id
		it should respond with a 404 error if <id> is not found
		it should contain the drink.long() data representation
		returns status code 200 and json {"success": True, "movies": movie}
		where movie is the details of updated movie
		or appropriate status code indicating reason for failure
	'''

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie_by_id(jwt, movie_id):
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:
            data = json.loads(request.data)
            if 'title' in data:
                movie.title = data['title']

            if 'date' in data:
                movie.date = data['date']

            movie.update()
            return jsonify(
                {
                    'success': True,
                    'movies': movie.format()
                }), 200

        except ex:
            abort(500)

    '''
	@TODO implement endpoint
	    DELETE /movies/<id>
		where <id> is the existing model id
		it should respond with a 404 error if <id> is not found
		it should delete the corresponding row for <id>
		it should require the 'delete:movies' permission
		returns status code 200 and json {"success": True, "delete": id}
		where id is the id of the deleted record
		or appropriate status code indicating reason for failure
	'''

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:
            movie.delete()

            return jsonify(
                {
                    'success': True,
                    'delete': movie.id
                }), 200

        except ex:
            db.session.rollback()
            abort(500)

    # Error Handling
    '''
	Example error handling for unprocessable entity
	'''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "success": False,
                "error": 422,
                "message": "unprocessable"
            }), 422

    '''
	@TODO implement error handlers using the @app.errorhandler(error) decorator
	    each error handler should return (with appropriate messages):
		     jsonify({
			    "success": False,
			    "error": 404,
			    "message": "resource not found"
			    }), 404

	'''

    '''
	@TODO implement error handler for 404
	    error handler should conform to general task above
	'''

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    '''
	@TODO implement error handler for AuthError
	    error handler should conform to general task above
	'''

    @app.errorhandler(AuthError)
    def process_AuthError(Err):
        return jsonify({
            "success": False,
            "error": Err.status_code,
            "message": Err.error['description']
        }), Err.status_code

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run()
