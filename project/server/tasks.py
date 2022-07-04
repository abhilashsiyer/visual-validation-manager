import os
import time

from celery import Celery
from flask import jsonify

from image_kit.file_uploader import upload_image
from image_kit.retrieve_file import get_file_url
from opencv_image.image_compare import url_to_image, validate_image

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task")
def init_type(task_type):
    time.sleep(int(task_type) * 10)
    return False


@celery.task(name="validate_image")
def visual_validation(file_tag, file_path):
    # Add logic to check if base exists
    print ('fileTag')
    print (file_tag)
    existing_file_url = get_file_url(file_tag)
    print('existing_file_url')
    print(existing_file_url)
    if existing_file_url:
        image_to_compare_url = upload_image(file_path, "to_compare"+file_tag)
        print('image_to_compare_url')
        print(image_to_compare_url)
        response = validate_image(existing_file_url, image_to_compare_url)
        return response
    else:
        url = upload_image(file_path, file_tag)
        return {'message': 'File uploaded as base', "base_image_url": url, "validation_result": True}

    # If yes, then compare
    # If not then upload file to imageKit URL and return true
