import re


class Validator():

    def valid_username(self, username):
        '''validator to ensure that username
        input matches the string structure'''
        username_pattern = re.compile(
            r'^[a-zA-Z_]+([a-zA-Z0-9]{1,10})$'
            )
        if username_pattern.match(username):
            return True
        return False

    def valid_password(self, password):
        '''validate to ensure that password
         has a characters and one to nine'''
        password_pattern = re.compile(r'^[a-zA-Z0-9]{6,25}$')
        if password_pattern.match(password):
            return True
        return False

    def valid_email(self, email):
        '''validate email matches a certain 
        pattern i. doe@andela.com'''
        email_pattern = re.compile(
            r'(^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]+$)'
            )
        if email_pattern.match(email):
            return True
        return False

    def q_validate(q):
        q_pattern = re.compile(r'^[a-zA-Z\s]+')
        if q_pattern.match(q):
            return True
        return False
