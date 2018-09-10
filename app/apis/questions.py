from flask_restplus import Namespace
from flask_restplus import Resource

api = Namespace('questions', description='question related functionalities')


@api.route('')
class Questions(Resource):
    def post(self):
        return{"post a question": "post a question"}

    def get(self):
        return{"get ": "get all question"}

@api.route('/<questionid>')
class Questionwithid(Resource):
    def get(self):
        return{"get": "get a specific question"}

    def delete(self):
        return{"delete": "delete a specific question with all answers"}

@api.route('/<questionid>/answers')
class QuestionPostAnswer(Resource):
    def post(self):
        return{"get": "get a specific question"}

@api.route('/<questionid>/answers/<answerid>')
class QuestionAnswerAccept(Resource):
    def put(self):
        return{"get": "get a specific question"}
