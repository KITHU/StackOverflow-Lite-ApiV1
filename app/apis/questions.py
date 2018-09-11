"""This module holds question related operations
it has post a question, get all questions
delete a question"""
from flask_restplus import Namespace
from flask_restplus import Resource
from flask_restplus import reqparse
from flask_restplus import fields
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from app.models import Database
from utils.validate import Validator

api = Namespace('questions', description='question related functionalities')

qst_model = api.model('ask question', {
    'title': fields.String(required=True,
                           description='title is required'),
    'description': fields.String(required=True,
                                 description='description is required')})

qst_arg = reqparse.RequestParser()
qst_arg.add_argument(
            'title',
            type=str, required=True,
            help="title is required"
            )
qst_arg.add_argument(
            'description',
            type=str, required=True,
            help="description is required"
            )


@api.route('')
class Questions(Resource):
    """this class deals with posting a question and
     get all questions. it has two routes"""
    @api.expect(qst_model)
    @jwt_required
    def post(self):
        """This routes post a new question if it does not exist"""
        valid = Validator()
        db = Database()
        qst_input = qst_arg.parse_args()
        title = qst_input['title']
        description = qst_input['description']
        if valid.q_validate(title) is False:
            return{"error": "title is invalid"}, 400
        if valid.q_validate(description) is False:
            return{"error": "description is invalid"}, 400
        if db.get_by_argument('questions', 'description', description):
            return {'message': 'question already exists'}, 409
        if db.get_by_argument('questions', 'title', title):
            return {'message': 'question already exists'}, 409

        user_id = get_jwt_identity()
        db.insert_question_data(user_id, title, description)
        return{"message": "Question created successfully"}, 201

    @jwt_required
    def get(self):
        """This route returns all avalable questions"""
        db = Database()
        questions = db.fetch_all()
        if len(questions) < 1:
            return{"message": "There are no questions Ask"}, 404
        return{"All_Questions": questions}


@api.route('/<int:questionid>')
class Questionwithid(Resource):
    """this class has routes for get a question
    by id and delete a question """
    def get(self, questionid):
        return{"get": questionid}

    @jwt_required
    def delete(self, questionid):
        """this routes delete a question and all answers provided"""
        db = Database()
        user_id = get_jwt_identity()
        questions = db.get_by_argument('questions', 'question_id', questionid)
        if questions:
            if user_id in questions:
                db.delete_question(questionid)
                return{'message':
                       'Question deleted successfully and answers'}, 200
            return{'Warning':
                   'You have no rights to delete this question'}, 403
        return{'message': 'No question by that id'}, 404
        

@api.route('/<questionid>/answers')
class QuestionPostAnswer(Resource):
    def post(self):
        return{"get": "get a specific question"}


@api.route('/<questionid>/answers/<answerid>')
class QuestionAnswerAccept(Resource):
    def put(self):
        return{"get": "get a specific question"}
