import os

from flask import Flask, request, abort

from app.core.config import settings
from app.db.services import TaskService
from app.schemas.form import TaskAAddForm, TaskUpdateForm

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.flask_settings.secret_key


@app.route('/task', methods=['POST'])
async def add_task():
    form = TaskAAddForm()
    data = form.data.copy()
    del data['csrf_token']
    if not data['title'] or not data['description']:
        abort(400)
    task = await TaskService().add_one(data=data)
    return task, 201


@app.route('/tasks/<id>', methods=['GET', 'PUT', 'DELETE'])
async def get_task_by_id(id: int):
    try:
        if int(id) <= 0:
            abort(400)
    except ValueError:
        abort(400)
    if request.method == 'GET':
        task = await TaskService().find_one(task_id=id)
        return task
    if request.method == 'PUT':
        form = TaskUpdateForm()
        data = form.data.copy()
        del data['csrf_token']
        task = await TaskService().update(task_id=id, data=data)
        return task
    if request.method == 'DELETE':
        await TaskService().delete(task_id=id)
        return {'ok': True}


@app.route('/tasks', methods=['GET'])
async def get_all_tasks():
    tasks = await TaskService().find_all()
    return tasks


@app.errorhandler(404)
async def not_found(error):
    return {
        'status': 'error',
        'details': 'Not Found'
    }, 404


@app.errorhandler(400)
async def bed_request(error):
    return {
        'status': 'error',
        'details': 'Bad Request'
    }, 400

if __name__ == '__main__':
    app.run(port=settings.flask_settings.port, debug=True)

