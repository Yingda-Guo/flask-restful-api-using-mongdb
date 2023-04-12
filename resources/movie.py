from flask import Response, request
from database.models import Movie, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, fields
from app import api

from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import SchemaValidationError, MovieAlreadyExistsError, InternalServerError, UpdatingMovieError, DeletingMovieError, MovieNotExistsError

# api document format
movie_model = api.model("Movie Record",{
   'name':fields.String,
   'casts':fields.List(fields.String),
   'genres':fields.List(fields.String)
})

class MoviesApi(Resource):
  def get(self):
    movies = Movie.objects().to_json()
    return Response(movies, mimetype="application/json", status=200)
  
  @jwt_required()
  @api.doc(security='apikey', body = movie_model)
  def post(self):
    try:
        user_id = get_jwt_identity()
        body = request.get_json(force=True)
        user = User.objects.get(id=user_id)
        movie = Movie(**body, added_by=user)
        movie.save()
        user.update(push__movies=movie)
        user.save()
        id = movie.id
        return {'id': str(id)}, 200
    except (FieldDoesNotExist, ValidationError):
       raise SchemaValidationError
    except NotUniqueError:
       raise MovieAlreadyExistsError
    except Exception as e:
       raise InternalServerError

class MovieApi(Resource):
  @jwt_required()
  @api.doc(security='apikey', body = movie_model)
  def put(self, id):
    try:
        user_id = get_jwt_identity()
        movie = Movie.objects.get(id=id, added_by=user_id)
        body = request.get_json(force=True)
        movie.update(**body)
        return  {'id': str(id), 'status': 'updated'}, 200
    except InvalidQueryError:
        raise SchemaValidationError
    except DoesNotExist:
        raise UpdatingMovieError
    except Exception:
        raise InternalServerError  
  
  @jwt_required()
  @api.doc(security='apikey')
  def delete(self, id):
    try:
        user_id = get_jwt_identity()
        movie = Movie.objects.get(id=id, added_by=user_id)
        movie.delete()
        return {'id': str(id), 'status': 'deleted'}, 200
    except DoesNotExist:
       raise DeletingMovieError
    except Exception:
       raise InternalServerError
  
  @api.doc(params={'id': 'Movie ID'}, security='apikey')
  @jwt_required()
  def get(self, id):
    try:
        movies = Movie.objects.get(id=id).to_json()
        return Response(movies, mimetype="application/json", status=200)
    except DoesNotExist:
       raise MovieNotExistsError
    except Exception:
       raise InternalServerError
