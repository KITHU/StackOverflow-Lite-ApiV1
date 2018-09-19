"""Database queries"""
import os
import psycopg2


class Database:
    """class that holds all database related queries
       tables are created and used here"""

    def __init__(self):
        """initializes the connection to the db"""

        config = os.getenv('APP_SETTINGS')
        host = os.getenv('DB_HOST')
        user = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD')

        if config == 'testing':
            database_name = os.getenv('TEST_DB')
        else:
            database_name = os.getenv('DB_NAME')
        self.connection = psycopg2.connect(
            database=database_name,
            user=user,
            password=password,
            host=host
        )
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """creates all the tables for the db"""
        query = """
        CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(85) NOT NULL,
        PRIMARY KEY (user_id)
        )
        """
        self.cursor.execute(query)

        query = """ CREATE TABLE IF NOT EXISTS questions (
        question_id SERIAL,
        user_id INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        date TIMESTAMP DEFAULT now(),
        PRIMARY KEY (question_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """
        self.cursor.execute(query)

        query = """
        CREATE TABLE IF NOT EXISTS answers (
        answer_id SERIAL,
        question_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        reply TEXT NOT NULL,
        preffered VARCHAR(30) DEFAULT 'False',
        up_vote INTEGER DEFAULT 0,
        down_vote INTEGER DEFAULT 0,
        PRIMARY KEY (answer_id),
        FOREIGN KEY (question_id) REFERENCES \
        questions(question_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def insert_user_data(self, username, email, password):
        """insert new user data to database i.e create user"""
        user_query = "INSERT INTO users (username, email, password) VALUES\
         ('{}', '{}', '{}');".format(username, email, password)
        self.cursor.execute(user_query)
        self.connection.commit()

    def get_by_argument(self, table, column_name, argument):
        """universal method to query database by one field"""
        query = "SELECT * FROM {} WHERE {} = '{}';".format(table,
                                                           column_name,
                                                           argument)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result

    def insert_answer_data(self, question_id, reply, user_id):
        """Insert a new answer to a specific question
        in the database"""
        query = "INSERT INTO answers (question_id, reply, user_id)\
         VALUES('{}','{}', '{}' );".format(question_id, reply, user_id)
        self.cursor.execute(query)
        self.connection.commit()

    def fetch_all(self):
        """ Fetches all questions from the database"""
        self.cursor.execute("SELECT * FROM questions ")
        rows = self.cursor.fetchall()
        questions = []
        for row in rows:
            row = {'question_id': row[0], 'user_id': row[1],
                   'title': row[2],
                   'description': row[3],
                   'date posted': str(row[4])
                   }
            questions.append(row)
        return questions

    def query_all_where_id(self, table_name, table_column, item_id):
        """method selects all records from a database matching a value
        select * from table_name where table_column = item_id"""
        self.cursor.execute("(SELECT * FROM {} WHERE {} = '{}');".format(
            table_name, table_column, item_id))
        items = self.cursor.fetchall()
        return items

    def insert_question_data(self, user_id, title, description):
        """Insert a new question to the database"""
        query = "INSERT INTO questions (user_id, title, description)\
         VALUES('{}','{}', '{}' );".format(user_id, title, description)
        self.cursor.execute(query)
        self.connection.commit()

    def delete_question(self, question_id):
        """method deletes question from database"""
        delete_query = "DELETE FROM questions WHERE question_id = {}" .format(
            question_id)
        self.cursor.execute(delete_query)
        self.connection.commit()

    def update_answer_record(self,
                             table_name, set_column,
                             new_value, where_column, item_id):
        """method updates record. i.e UPDATE table_name SET set_column =
         new_value, wherewhere_colum = item_id"""
        updt = "Update {} SET {} = '{}' WHERE {} = '{}'".format(table_name,
                                                                set_column,
                                                                new_value,
                                                                where_column,
                                                                item_id)
        self.cursor.execute(updt)
        self.connection.commit()

    def drop_tables(self):
        """method drops all tables in database"""
        self.cursor.execute("""DROP TABLE IF EXISTS users CASCADE""")
        self.cursor.execute("""DROP TABLE IF EXISTS questions CASCADE""")
        self.cursor.execute("""DROP TABLE IF EXISTS answers CASCADE""")
        self.connection.commit()
