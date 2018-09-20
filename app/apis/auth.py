"""this module has routes for signup and login"""
from flask_restplus import Namespace
from flask_restplus import fields
from flask_restplus import Resource
from flask_restplus import reqparse
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from utils.validate import Validator
from app.models import Database

api = Namespace('auth', description='user related functionalities')
bcrypt = Bcrypt()

signup_model = api.model('auth signup', {
    'username': fields.String(required=True, description='username'),
    'email': fields.String(required=True, description='email'),
    'password': fields.String(required=True, description='password')})

login_model = api.model('auth login', {
    'email': fields.String(required=True, description='email'),
    'password': fields.String(required=True, description='password')})
# signup parser
signup_arg = reqparse.RequestParser()
signup_arg.add_argument(
                        'username',
                        type=str,
                        required=True,
                        help='usernae is required!'
                        )
signup_arg.add_argument(
                        'email',
                        type=str, required=True,
                        help="email is required"
                        )
signup_arg.add_argument(
                        'password',
                        type=str, required=True,
                        help="password is required"
                        )
# login parser
login_arg = reqparse.RequestParser()
login_arg.add_argument(
                       'email',
                       type=str, required=True,
                       help="email is required"
                       )
login_arg.add_argument(
                       'password',
                       type=str, required=True,
                       help="password is required"
                       )


@api.route('/signup')
class Signup(Resource):
    """signup route hosted by this route"""
    @api.expect(signup_arg)
    def post(self):
        """user needs username, valid email and
           password to signup"""
        valid = Validator()
        db = Database()
        user_data = signup_arg.parse_args()
        username = user_data['username']
        email = user_data['email']
        password = user_data['password']
        if valid.valid_username(username) is False:
            return {"error": "invalid username"}, 400
        if valid.valid_email(email) is False:
            return {"error": "invalid email"}, 400
        if valid.valid_password(password) is False:
            return {"error": "invalid password"}, 400
        if db.get_by_argument('users', 'email', email):
            return {'message': 'user already exists'}, 409
        hashed_pass = bcrypt.generate_password_hash(password).decode('utf-8')
        db.insert_user_data(username, email, hashed_pass)
        return{"message": "Account created"}, 201


@api.route('/login')
class Login(Resource):
    """user can login using this route"""
    @api.expect(login_model)
    def post(self):
        """user needs email used to signup
        and password to login"""
        valid = Validator()
        db = Database()
        user_data = login_arg.parse_args()
        email = user_data['email']
        password = user_data['password']

        if valid.valid_email(email) is False:
            return {"error": "invalid email"}, 400
        if valid.valid_password(password) is False:
            return {"error": "invalid password:check length"}, 400
        user = db.get_by_argument('users', 'email', email)
        if user == None:
            return{"error": "wrong email address"}, 404
        if(email == user[2] and
           bcrypt.check_password_hash(user[3], password) is False):
            return {"error": "wrong password"}, 400

        if(email != user[2] and
           bcrypt.check_password_hash(user[3], password) is False):
            return {"error": "invalid login credentials"}, 400

        if(email == user[2] and
           bcrypt.check_password_hash(user[3], password) is True):
            access_token = create_access_token(identity=user[0],
            expires_delta=False)
            return {"message": "login successful",
                    "username": user[1],
                    "userid": user[0],
                    "access_token": access_token}, 200
