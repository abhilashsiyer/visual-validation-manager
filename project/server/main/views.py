# project/server/main/views.py
import os
from celery.result import AsyncResult
from flask import Blueprint, jsonify, request

from project.server.tasks import init_type, visual_validation
from werkzeug.utils import secure_filename

main_blueprint = Blueprint("main", __name__, )

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_blueprint.route("/tasks", methods=["POST"])
def run_task():
    content = request.json
    task_type = content["type"]
    task = init_type.delay(int(task_type))
    return jsonify({"task_id": task.id}), 202


@main_blueprint.route("/upload-file-for-validation", methods=["POST"])
def upload_file_for_validation():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    file_tag = request.form['tag']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        current_dir = os.getcwd()
        print("current_dir", current_dir)
        file_path = os.path.join(current_dir + "/uploads", filename)
        print("file_path", file_path)
        file.save(file_path)
        task = visual_validation.delay(file_tag,file_path)
        resp = jsonify({'message': 'File received for processing', "task_id": task.id})
        resp.status_code = 202
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result), 200
