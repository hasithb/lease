from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from flask import current_app
from .celery_worker import celery
from .models import Result
from .utils import process_text_file, extract_key_clauses
from celery.utils.log import get_task_logger
from sqlalchemy.exc import IntegrityError
from .__init__ import db

@celery.task(bind=True, max_retries=3, soft_time_limit=300, name='app.tasks.analyze_lease_document_background')
def analyze_lease_document_background(self, lease_text_dict):
    logger = get_task_logger(__name__)
    try:
        logger.info("Task started...")

        with current_app.app_context():
            logger.info("Inside app context...")

            self.update_state(state='PROCESSING', meta={'progress': 'Extracting clauses...'})
            logger.info("Extracting clauses...")

            extracted_clauses = extract_key_clauses(" ".join(lease_text_dict.values()))
            logger.info("Clauses extracted, saving to DB...")

            result = Result(clauses=extracted_clauses)
            db.session.add(result)
            db.session.commit()
            logger.info("DB commit successful!")

            self.update_state(state='SUCCESS', meta={'progress': 'Analysis complete!'})
            logger.info("Task completed successfully!")
            return {'status': 'Success', 'result_id': result.id}

    except SoftTimeLimitExceeded as e:
        current_app.logger.error(f"Soft time limit exceeded: {str(e)}")
    except IntegrityError as e:
        try:
            db.session.rollback()
        except Exception as ex:
            logger.error(f"Failed to rollback: {str(ex)}")
        logger.error(f"Database integrity error: {str(e)}")
    except Exception as e:
        try:
            db.session.rollback()
        except Exception as ex:
            logger.error(f"Failed to rollback: {str(ex)}")
        self.retry(exc=e, countdown=2 ** self.request.retries)  # exponential backoff retry
        logger.error(f"Error in task: {str(e)}")
        return {'status': 'Failure', 'error_message': str(e)}




@celery.task(bind=True)
def long_running_task(self):
    # Your task logic here...
    return 'Task completed!'

@celery.task(bind=True)
def process_text_file_task(self, file_path):
    return process_text_file(file_path)