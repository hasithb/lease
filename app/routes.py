import joblib
import os
from flask import Blueprint, render_template, flash, jsonify, current_app
from .forms import LeaseForm
from . import db  # Import db from app/__init__.py
from werkzeug.utils import secure_filename
from app.utils import allowed_file, process_text_file
from .models import Result
import traceback
from celery.exceptions import NotRegistered

bp = Blueprint('routes', __name__)

# Loading other necessary models and data
model = joblib.load('lease_clause_classifier.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
KEY_CATEGORIES = ['Rent', 'Security Deposit', 'Maintenance', 'Termination']
PROBLEMATIC_CATEGORIES = ['Insurance', 'Sublease', 'Indemnity', 'Default']


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/register')
def register():
    return render_template('register.html')


from .tasks import analyze_lease_document_background

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bp.route('/upload_lease', methods=['GET', 'POST'])
def upload_lease():
    form = LeaseForm()
    if form.validate_on_submit():
        file = form.lease_file.data
        if file and allowed_file(file.filename):  # Ensure allowed_file is defined
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file_path = os.path.join(upload_folder, filename)

            try:
                file.save(file_path)
                logger.info("File saved successfully. About to enqueue task.")

                task = analyze_lease_document_background.apply_async(args=[file_path])  # Use apply_async
                logger.info(f"Task enqueued with ID: {task.id}")

                return jsonify({"task_id": task.id}), 202
            except Exception as e:
                error_info = traceback.format_exc()  # Get the traceback info
                logger.error(f"Error: {str(e)}\n{error_info}")  # Log error with traceback
                flash('An error occurred while uploading/processing the file.', 'error')
        else:
            flash('Invalid file type. Please upload a valid file.', 'error')
    return render_template('upload_lease.html', form=form)



@bp.route('/task-status/<task_id>')
def task_status(task_id):
    try:
        task = analyze_lease_document_background.AsyncResult(task_id)
        response_data = {
            'state': task.state,
            'result': task.info.get('result', '') if task.info else '',
            'progress': task.info.get('progress', 0) if task.info else 0,
            'error': task.info.get('error', '') if task.info else ''
        }
    except NotRegistered:
        response_data = {
            'state': 'ERROR',
            'result': '',
            'progress': 0,
            'error': f'Task with ID {task_id} not registered'
        }
    except Exception as e:
        response_data = {
            'state': 'ERROR',
            'result': '',
            'progress': 0,
            'error': str(e)
        }
    return jsonify(response_data)


@bp.route('/analysis_results/<int:result_id>', methods=['GET'])
def analysis_results(result_id):
    # TODO: Retrieve result_data using result_id from the database
    result_data = {}
    return render_template('analysis_results.html', result_data=result_data)


@bp.route('/task/<task_id>')
def background_task_status(task_id):
    from .tasks import analyze_lease_document_background
    # Ensure analyze_lease_document_background is defined in your code.
    task = analyze_lease_document_background.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the custom status
        }
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'status': str(task.info),  # this contains exception info
        }
    return jsonify(response)

def test_allowed_file():
    assert allowed_file("document.pdf")
    assert not allowed_file("document.exe")

bp.route("/healthz/db", methods=["GET"])
def check_db():
    try:
        # execute a simple query to check the database connectivity
        db.session.execute('SELECT 1;')
        return jsonify({"status": "up"}), 200
    except Exception as e:
        return jsonify({"status": "down", "error": str(e)}), 500

bp.route("/healthz/celery", methods=["GET"])
def check_celery():
    try:
        # Inspect all registered workers
        i = current_app.celery.control.inspect()
        if not i.stats():
            raise ValueError("No running Celery workers were found.")
        return jsonify({"status": "up"}), 200
    except Exception as e:
        return jsonify({"status": "down", "error": str(e)}), 500

bp.route("/healthz/broker", methods=["GET"])
def check_broker():
    try:
        # Check the broker's (e.g., Redis) connectivity
        info = current_app.celery.connection().default_channel.client.info()
        if 'redis_version' not in info:
            raise ValueError("Not connected to Redis.")
        return jsonify({"status": "up"}), 200
    except Exception as e:
        return jsonify({"status": "down", "error": str(e)}), 500
