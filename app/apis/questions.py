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

# answer reqparse
ans_arg = reqparse.RequestParser()
ans_arg.add_argument(
                     'answer',
                     type=str, required=True,
                     help="answer is required"
                     )
ans_model = api.model('answer question', {
    'answer': fields.String(required=True,
                            description='answer is required')})

# modify answer reqpase
modify_arg = reqparse.RequestParser()
modify_arg.add_argument(
                        'answer',
                        type=str, required=False,
                        help="modify answer"
                        )
modify_arg.add_argument(
                        'preffered',
                        type=str, required=False,
                        help="preffered set to True"
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
    @jwt_required
    def get(self, questionid):
        """route to get a single question by id and
        all the available answers"""
        db = Database()
        questions = db.get_by_argument('questions', 'question_id', questionid)
        if questions:
            question = {"question_id": questions[0],
                        "title": questions[2],
                        "description": questions[3],
                        "date posted": str(questions[4])}
            answers = db.query_all_where_id('answers',
                                            'question_id', questionid)

            answerlist = []
            for ans in answers:
                answerdic = {"answer_id": ans[0],
                             "question_id": ans[1],
                             "user_id": ans[2],
                             "answer": ans[3],
                             "preffered": ans[4],
                             "up_vote": ans[5],
                             "down_vote": ans[6]
                             }
                answerlist.append(answerdic)
            return{"question": question,
                   "answers": answerlist}, 200
        return{"message": "no question by that id"}, 400

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


@api.route('/<int:questionid>/answers')
class QuestionPostAnswer(Resource):
    """this class has method to provide answers to
    questions in the database"""
    @api.expect(ans_model)
    @jwt_required
    def post(self, questionid):
        """method to post a question answer
        anybody can post an answer to a question"""
        valid = Validator()
        db = Database()
        user_id = get_jwt_identity()
        ans_input = ans_arg.parse_args()
        user_answer = ans_input['answer']
        if valid.q_validate(user_answer) is False:
            return{"message": "answer must contain leters"}, 400
        if db.get_by_argument("questions", "question_id", questionid):
            if db.get_by_argument('answers', 'reply', user_answer):
                return {'message': 'That answer already exists'}, 409
            db.insert_answer_data(questionid, user_answer, user_id)
            return{"message": "Your answer was posted successfully"}, 201
        return{"message": "question id does not exist"}, 404


@api.route('/<questionid>/answers/<answerid>')
class QuestionAnswerAccept(Resource):
    """class to host method to modify answer if current user
    is the owner or mark answer accepted"""
    @api.expect(modify_arg)
    @jwt_required
    def put(self, questionid, answerid):
        """modify answer or mark it as preffered"""
        db = Database()
        valid = Validator()
        user_id = get_jwt_identity()
        answer = db.get_by_argument("answers", "question_id", questionid)
        if answer:
            if user_id == answer[2]:
                preffered = modify_arg.parse_args()
                preffer = preffered['preffered']
                if preffer != "True":
                    return{"message": "preffered has no value True"}, 400
                db.update_answer_record("answers", "preffered", preffer,
                                        "answer_id", answerid)
                return{"message": "answer marked as preffered"}, 200

            answer1 = db.get_by_argument("answers", "answer_id", answerid)
            if answer1:
                if user_id == answer1[2]:
                    modifyans = modify_arg.parse_args()
                    eddited_ans = modifyans["answer"]
                    if valid.q_validate(eddited_ans) is False:
                        return{"message": "answer should contain letters"}
                    db.update_answer_record("answers", "reply", eddited_ans,
                                            "answer_id", answerid)
                    return{"message": "answer updated sucessfully"}, 200
        return{"message": "warning you are not authorized"}, 403

    @api.route("/userquestions")
    class AllUserQuestions(Resource):
        """will fetch all questions a user have posted"""
        @jwt_required
        def get(self):
            """all questions by the current user"""
            db = Database()
            user_id = get_jwt_identity()
            questions = db.query_all_where_id("questions", "user_id", user_id)
            if questions:
                user_qst = []
                for qst in questions:
                    question = {"question_id": qst[0], "user_id": qst[1],
                                "title": qst[2], "description": qst[3],
                                "date": str(qst[4])}
                user_qst.append(question)
                return{"total_questions": len(user_qst),
                       "questions": question}, 200
            return{"total_questions": 0}, 200

    @api.route("/useranswers")
    class AllUserAnswers(Resource):
        """will fetch all questions a user have posted"""
        @jwt_required
        def get(self):
            """all answers by the current user"""
            db = Database()
            user_id = get_jwt_identity()
            answers = db.query_all_where_id("answers", "user_id", user_id)
            if answers:
                ans_list = []
                for ans in answers:
                    answerdic = {"answer_id": ans[0],
                                 "question_id": ans[1],
                                 "user_id": ans[2],
                                 "answer": ans[3],
                                 "preffered": ans[4],
                                 "up_vote": ans[5],
                                 "down_vote": ans[6]
                                 }
                    ans_list.append(answerdic)
                return{"total_answers": len(ans_list),
                       "user_answers": ans_list}, 200
            return{"total_answers": 0}, 200
