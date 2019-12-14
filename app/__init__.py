from . import configs
from flask import Flask
from flask_cors import CORS
from flask_redis import FlaskRedis
import os
import pymysql

root_dir = os.path.dirname(os.path.abspath(__file__))
redis_store = FlaskRedis()

ninja_token = os.environ.get("NINJA_TOKEN",os.getenv('NINJA_TOKEN'))
conn = pymysql.connect(host=os.environ.get("MYSQL_HOST",os.getenv('FLASK_MYSQL_HOST')),
                        user=os.environ.get("MYSQL_USER",os.getenv('FLASK_MYSQL_USER')),
                        password=os.environ.get("MYSQL_PASSWORD",os.getenv('FLASK_MYSQL_PASSWORD')),
                        db=os.environ.get("MYSQL_DB",os.getenv('FLASK_MYSQL_DB')),
                        cursorclass=pymysql.cursors.DictCursor,
                        autocommit=True)
db = conn.cursor()


def create_app():
    app = Flask(__name__)
    app.config.from_object(configs.Config)
    app.secret_key = os.environ.get("SECRET_KEY",os.getenv('SECRET_KEY'))

    redis_store.init_app(app)

    #registering CORS API
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # registering controllers
    from .controllers import api_blueprint
    app.register_blueprint(api_blueprint)

    return app


