from flask import request, Response
from flask_jwt_extended import create_access_token
from database.models import User
from flask_restx import Resource, fields
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, InternalServerError
from app import api

# api doc
sign_model = api.model("SignIn",{
   'email':fields.String,
   'password':fields.String
})

class SignupApi(Resource):
 @api.doc(body = sign_model)
 def post(self):
    try:
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        user.save()
        id = user.id
        return {'id': str(id)}, 200
    except FieldDoesNotExist:
        raise SchemaValidationError
    except NotUniqueError:
        raise EmailAlreadyExistsError
    except Exception as e:
        raise InternalServerError
 
class LoginApi(Resource):
  @api.doc(body = sign_model)
  def post(self):
    try:
        body = request.get_json()
        user = User.objects.get(email=body.get('email'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
           return {'error':'Email or password invalid'}, 401
        
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity = str(user.id), expires_delta = expires)
        return {'token':access_token, 'token bearer': 'Bearer ' + str(access_token)}, 200
    except (UnauthorizedError, DoesNotExist):
        raise UnauthorizedError
    except Exception as e:
        raise InternalServerError