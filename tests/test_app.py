"""test module that test methods in the Model class
and also the api routes in the qustions.py"""
import unittest
from flask import json
from app.models import Database
from app import create_app

db = Database()
db.drop_tables()
db.create_tables()


class TestModels(unittest.TestCase):
    """class to hold test ...test models and routes"""
    def setUp(self):
        """setup method for tests"""
        app = create_app('testing')
        self.tester = app.test_client(self)

        self.newuser = {"username": "martin",
                        "email": "martin@yahoo.com",
                        "password": "martin1"}

        self.new_user = {"username": "james",
                         "email": "james@yahoo.com",
                         "password": "james1"}

        self.user1 = {"username": "james",
                      "email": "james@yahoo",
                      "password": "james1"}

        self.user2 = {"username": "james",
                      "email": "james@yahoo.com",
                      "password": "111"}

        self.user3 = {"username": "j",
                      "email": "james@yahoo.com1",
                      "password": "james1"}
        
        self.qst1 = {"title": "math calculus",
                     "description": "different methods exists"}
        self.qst2 = {"title": " ",
                     "description": "different methods exists"} 
        self.qst3 = {"title": "api auth",
                     "description": "jwt vs flask_jwt_extended?"}            
        self.answer1 = {"answer": "different methods exists all over"}
        self.answer11 = {"answer": "machine learning algorithms"}
        self.answer2 = {"answer": " "}
        self.modify_answer1 = {"answer": "A day with data science engineer",
                               "preffered": "True"}

    def test_api_can_create_new_account(self):
        """test api signup related functinalities and error handling"""
        res = self.tester.post("/api/v1/auth/signup", data=self.new_user)
        self.assertEqual(res.status_code, 201)

        reso = self.tester.post("/api/v1/auth/signup", data=self.newuser)
        self.assertEqual(reso.status_code, 201)

        res1 = self.tester.post("/api/v1/auth/signup", data=self.user1)
        self.assertEqual(res1.status_code, 400)

        res2 = self.tester.post("/api/v1/auth/signup", data=self.user2)
        self.assertEqual(res2.status_code, 400)

        res3 = self.tester.post("/api/v1/auth/signup", data=self.user3)
        self.assertEqual(res3.status_code, 400)

    def test_api_can_signin_user(self):
        """test api login related functinalities and error handling"""
        ress = self.tester.post("/api/v1/auth/login", data=self.new_user)
        self.assertEqual(ress.status_code, 200)

        ress1 = self.tester.post("/api/v1/auth/login", data=self.user1)
        self.assertEqual(ress1.status_code, 400)

        ress2 = self.tester.post("/api/v1/auth/login", data=self.user2)
        self.assertEqual(ress2.status_code, 400)

        ress3 = self.tester.post("/api/v1/auth/login", data=self.user3)
        self.assertEqual(ress3.status_code, 404)

    def test_api_can_post_a_question(self):
        res = self.tester.post("/api/v1/auth/login", data=self.new_user)
        reply = json.loads(res.data.decode())
        token = reply["access_token"]
        headers = {'Authorization': 'Bearer ' + token}
        res1 = self.tester.post("/api/v1/questions",
                                headers=headers,
                                content_type='application/json',
                                data=json.dumps(self.qst1))
        self.assertEqual(res1.status_code, 201)

        resz1 = self.tester.post("/api/v1/questions",
                                 headers=headers,
                                 content_type='application/json',
                                 data=json.dumps(self.qst3))
        self.assertEqual(resz1.status_code, 201)
        # send question that has no title
        ress1 = self.tester.post("/api/v1/questions",
                                 headers=headers,
                                 content_type='application/json',
                                 data=json.dumps(self.qst2))
        self.assertEqual(ress1.status_code, 400)
# test sending the same question that exist
        res2 = self.tester.post("/api/v1/questions",
                                headers=headers,
                                content_type='application/json',
                                data=json.dumps(self.qst1))
        self.assertEqual(res2.status_code, 409)
# test get all questions available
        res3 = self.tester.get("/api/v1/questions",
                               headers=headers,
                               content_type='application/json')
        self.assertEqual(res3.status_code, 200)
# test delete id that does not exist
        res4 = self.tester.delete("/api/v1/questions/8",
                                  headers=headers,
                                  content_type='application/json')
        self.assertEqual(res4.status_code, 404)
        ress4 = self.tester.delete("/api/v1/questions/2",
                                   headers=headers,
                                   content_type='application/json')
        self.assertEqual(ress4.status_code, 200)
# test post an answer to a non existing question id
        res5 = self.tester.post("/api/v1/questions/8/answers",
                                headers=headers,
                                content_type='application/json',
                                data=json.dumps(self.answer1))
        self.assertEqual(res5.status_code, 404)
        # send a valid answer to a valid id
        res6 = self.tester.post("/api/v1/questions/1/answers",
                                headers=headers,
                                content_type='application/json',
                                data=json.dumps(self.answer1))
        self.assertEqual(res6.status_code, 201)
        # send empty dictionary with key no value
        res7 = self.tester.post("/api/v1/questions/1/answers",
                                headers=headers,
                                content_type='application/json',
                                data=json.dumps(self.answer2))
        self.assertEqual(res7.status_code, 400)
        # send similar answer that alread exist
        res8 = self.tester.post("/api/v1/questions/1/answers",
                                headers=headers,
                                content_type='application/json',
                                data=json.dumps(self.answer1))
        self.assertEqual(res8.status_code, 409)
# test fetch a question and all available answers by id 
        ress3 = self.tester.get("/api/v1/questions/1",
                                headers=headers,
                                content_type='application/json')
        self.assertEqual(ress3.status_code, 200)
# test fetch all questions posted by the current user
        res9 = self.tester.get("/api/v1/questions/userquestions",
                               headers=headers,
                               content_type='application/json')
        self.assertEqual(res9.status_code, 200)

        resi9 = self.tester.get("/api/v1/questions/useranswers",
                                headers=headers,
                                content_type='application/json')
        self.assertEqual(resi9.status_code, 200)
# test if owner of the question can mark answer preffered
# owner of answer can update answer 
        res10 = self.tester.put("/api/v1/questions/4/answers/4",
                                headers=headers,
                                content_type='application/json')
        self.assertEqual(res10.status_code, 403)

        ress10 = self.tester.put("/api/v1/questions/1/answers/4",
                                 headers=headers,
                                 content_type='application/json')
        self.assertEqual(ress10.status_code, 400)

        resss10 = self.tester.put("/api/v1/questions/1/answers/4",
                                  headers=headers,
                                  content_type='application/json',
                                  data=json.dumps(self.modify_answer1))
        self.assertEqual(resss10.status_code, 200)

        # ressss10 = self.tester.put("/api/v1/questions/2/answers/1",
        #                            headers=headers,
        #                            content_type='application/json',
        #                            data=json.dumps(self.modify_answer1))
        # self.assertEqual(ressss10.status_code, 200)

    def test_using_a_new_user(self):
        res = self.tester.post("/api/v1/auth/login", data=self.newuser)
        reply = json.loads(res.data.decode())
        token = reply["access_token"]
        headers = {'Authorization': 'Bearer ' + token}

        res1 = self.tester.post("/api/v1/questions/1/answers",
                                headers=headers,
                                content_type='application/json',
                                data=json.dumps(self.answer11))
        self.assertEqual(res1.status_code, 201)

        res2 = self.tester.put("/api/v1/questions/1/answers/2",
                               headers=headers,
                               content_type='application/json',
                               data=json.dumps(self.modify_answer1))
        self.assertEqual(res2.status_code, 200)
# test user can upvote or down vote
        res3 = self.tester.post("/api/v1/votes/2/upvote",
                                headers=headers,
                                content_type='application/json')
        self.assertEqual(res3.status_code, 201)

        res4 = self.tester.post("/api/v1/votes/2/downvote",
                                headers=headers,
                                content_type='application/json')
        self.assertEqual(res4.status_code, 201)

        res33 = self.tester.post("/api/v1/votes/7/upvote",
                                 headers=headers,
                                 content_type='application/json')
        self.assertEqual(res33.status_code, 404)

        res44 = self.tester.post("/api/v1/votes/13/downvote",
                                 headers=headers,
                                 content_type='application/json')
        self.assertEqual(res44.status_code, 404)
# this user has no posted answers




