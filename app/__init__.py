from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_cors import CORS
from config import Config
import redis as redis_module

app = Flask(__name__)
app.config.from_object(Config)
# CORS(app)
db = SQLAlchemy(app)
redis = redis_module.Redis(host='localhost', port=6379, db=app.config['REDIS_DATABASE_ID'], decode_responses=True)
# migrate = Migrate(app, db)

from app import routes, models, utils
