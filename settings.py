from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///<your_database_location_uri>/flask-and-redis-application/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
