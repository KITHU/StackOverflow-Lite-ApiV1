# StackOverflow-Lite-ApiV1

[![Build Status](https://travis-ci.org/KITHU/StackOverflow-Lite-ApiV1.svg?branch=develop)](https://travis-ci.org/KITHU/StackOverflow-Lite-ApiV1)
[![Coverage Status](https://coveralls.io/repos/github/KITHU/StackOverflow-Lite-ApiV1/badge.svg?branch=develop)](https://coveralls.io/github/KITHU/StackOverflow-Lite-ApiV1?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/73317bbf8502c9e9b20a/maintainability)](https://codeclimate.com/github/KITHU/StackOverflow-Lite-ApiV1/maintainability)



# Description
StackOverflow-lite is a platform where users can ask questions and post answers to questions.

# Development
- This Application is powered by Python3 Language,  Flask and flask_restplus python flameworks
  
##### heroku link
- https://stackoverflow-lite-apiv1.herokuapp.com/api/v1/
##### github repo link
- https://github.com/KITHU/StackOverflow-Lite-ApiV1.git

## Features
- Users can signup
- Users can signin
- Users can post a question                       
- Users can get all questions
- Users can get a single question with its answers
- Users can delete a question
- Users can post answers to questions
- Users can mark an question answer as preffered
- Users can up vote or down vote answer
- Users can comment on an answer
### end points
Endpoints                          | features
---------------------------------- | -----------------------------------------------------------
POST api/auth/signup               | Register new user
POST api/auth/login                | Login user
GET  api/v1/questions              | returns all questions
GET  api/v1/questions/id           | returns a single question and all available answers
POST api/v1/questions              | post a question to app
POST api/v1/questions/id/answers   | post an answer to a question 
DETELE api/v1/questions/id         | delete a question and all the available answers

## local setup and testing using postman
1. create a python3 virtual environment 
2. clone the repo ..link given above
3. install dependances from requirements.txt
4. create a .env file and add this code
 ```  
   source env/bin/activate

   export APP_SETTINGS="development"
   export JWT_SECRET_KEY="this is secret"

```  
5. to run the app type python run.py from the console
6. to run test type pytest --cov-report term-missing --cov=app on the console

7. open postman and start testing the above endpoints

### sample body data for post, question and answer
i. answer 
```
{"answer":"your answer"}
```
ii. question 
```
{"title":"question title",
 "description":"your question content in full"}
```