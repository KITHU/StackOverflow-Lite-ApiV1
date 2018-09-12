"""this module has routes to vote an answer
   can up vote or downvote"""
from flask_restplus import Namespace
from flask_restplus import Resource
from flask_jwt_extended import jwt_required
from app.models import Database

api = Namespace('votes', description='vote related functionalities')


@api.route('/<answerid>/downvote')
class Downvote(Resource):
    """this class deals with logic to down vote
     an answer"""
    @jwt_required
    def post(self, answerid):
        """this route will downvote an answer"""
        db = Database()
        votes = db.get_by_argument("answers", "answer_id",)
        if votes:
            downvote = votes[6] + 1
            db.update_answer_record("answers", "down_vote",
                                    downvote, "answer_id", answerid)
            return{"message": "answer downvoted"}, 201
        return{"message": "No answer by that answer_id"}, 404


@api.route('/<answerid>/upvote')
class Downvote(Resource):
    """this class deals with logic to up vote
     an answer"""
    @jwt_required
    def post(self):
        """this route will upvote an answer"""
        db = Database()
        votes = db.get_by_argument("answers", "answer_id",)
        if votes:
            upvote = votes[5] + 1
            db.update_answer_record("answers", "up_vote",
                                    upvote, "answer_id", answerid)
            return{"message": "answer upvoted"}, 201
        return{"message": "No answer by that answer_id"}, 404
