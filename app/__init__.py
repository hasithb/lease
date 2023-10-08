import os
import logging
from celery import Celery
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from . import tasks

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logging.basicConfig(filename='app.log', level=logging.DEBUG)  # Log to a file

# Initialize extensions
db = SQLAlchemy()

def create_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        backend='redis://localhost:6380/1',
        broker='redis://localhost:6380/0',
        include=['app.tasks']
    )
    celery.conf.update(app.config)
    return celery

def raise_exception(msg):
    assert isinstance(msg, object)
    raise ValueError(msg)

def create_app() -> object:
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv('SECRET_KEY', 'your_secret_key'),
        CELERY_BROKER_URL=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6380/0'),
        CELERY_RESULT_BACKEND=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6380/1'),
        SQLALCHEMY_DATABASE_URI='sqlite:///results.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER='UPLOAD_FOLDER',
        broker_connection_retry_on_startup=True,
    )
    celery = create_celery(app)
    app.celery = celery

    # Assuming your blueprint is named 'bp' in your routes module
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    @app.route('/debug_env_vars')
    def debug_env_vars():
        broker_url = os.environ.get('CELERY_BROKER_URL')
        result_backend = os.environ.get('CELERY_RESULT_BACKEND')
        env_vars = {
            'CELERY_BROKER_URL': broker_url,
            'CELERY_RESULT_BACKEND': result_backend
        }
        return jsonify(env_vars)

    return app
