"""test module that test methods in the Model class
and also the api routes in the qustions.py"""
import unittest
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

    def test_api_can_create_new_account(self):
        """test api signup related functinalities and error handling"""
        res = self.tester.post("/api/v1/auth/signup", data=self.new_user)
        self.assertEqual(res.status_code, 201)

        res1 = self.tester.post("/api/v1/auth/signup", data=self.user1)
        self.assertEqual(res1.status_code, 400)

        res2 = self.tester.post("/api/v1/auth/signup", data=self.user2)
        self.assertEqual(res2.status_code, 400)

        res3 = self.tester.post("/api/v1/auth/signup", data=self.user3)
        self.assertEqual(res3.status_code, 400)

    def test_api_can_signin_user(self):
        ress = self.tester.post("/api/v1/auth/login", data=self.new_user)
        self.assertEqual(ress.status_code, 200)

        ress1 = self.tester.post("/api/v1/auth/login", data=self.user1)
        self.assertEqual(ress1.status_code, 400)

        ress2 = self.tester.post("/api/v1/auth/login", data=self.user2)
        self.assertEqual(ress2.status_code, 400)

        ress3 = self.tester.post("/api/v1/auth/login", data=self.user3)
        self.assertEqual(ress3.status_code, 404)
