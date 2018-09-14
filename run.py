import os
from app import create_app
from app.models import Database


config_name = os.getenv('APP_SETTINGS')  # config_name = "development"
app = create_app(config_name)

db = Database()
db.create_tables()

if __name__ == '__main__':
    app.run()
