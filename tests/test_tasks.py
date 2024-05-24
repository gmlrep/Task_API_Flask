# import pytest_asyncio
import asyncio
from datetime import datetime

import pytest
from httpx import AsyncClient

from app.db.database import async_engine, Base, async_session
from app.main import app


def get_time(time: str) -> str:
    time_hours = time.split(' ')[4]
    return f'{time_hours.split(":")[0]}:{time_hours.split(":")[1]}'


def test_add_task():
    with app.test_client() as client:

        body = {
            'title': 'new title',
            'description': 'some new description'
        }

        response = client.post('/task', data=body)
        assert response.status_code == 201
        assert response.json['title'] == body.get('title')
        assert response.json['description'] == body.get('description')

        body = {
            'title': 'new title',
        }
        response = client.post('/task', data=body)
        assert response.status_code == 400
        assert response.json['status'] == 'error'

        response = client.post('/task')
        assert response.status_code == 400
        assert response.json['status'] == 'error'


def test_get_task():
    with app.test_client() as client:
        response = client.get('/tasks/string')
        assert response.status_code == 400
        assert response.json['status'] == 'error'

        response = client.get('/tasks/1')
        assert response.status_code == 200
        assert response.json['id'] == 1

        response = client.get('/tasks/-34')
        assert response.status_code == 400
        assert response.json['status'] == 'error'


def test_put_task():
    with app.test_client() as client:
        body = {
            'title': 'edited title',
            'description': 'some edited description'
        }
        time_now = datetime.now().strftime('%H:%M')
        response = client.put('/tasks/1', data=body)
        assert response.status_code == 200
        assert response.json['title'] == body.get('title')
        assert response.json['description'] == body.get('description')
        update_at = get_time(response.json['update_at'])
        assert update_at == time_now

        response = client.put('/tasks/100')
        assert response.status_code == 404
        assert response.json == {"details": "Not Found", "status": "error"}

        body = {
            'title': 'edited name',
        }
        response = client.put('/tasks/1', data=body)
        assert response.status_code == 200
        assert response.json['title'] == body.get('title')
        update_at = get_time(response.json['update_at'])
        assert update_at == time_now

        body = {
            'description': 'some edited description'
        }
        response = client.put('/tasks/1', data=body)
        assert response.status_code == 200
        assert response.json['description'] == body.get('description')


def test_delete():
    with app.test_client() as client:
        body = {
            'title': 'new title',
            'description': 'some new description'
        }

        response = client.post('/task', data=body)
        assert response.status_code == 201
        assert response.json['title'] == body.get('title')
        assert response.json['description'] == body.get('description')
        task_id = response.json['id']

        response = client.delete(f'tasks/{task_id}')
        assert response.status_code == 200
        assert response.json['ok'] is True

        response = client.delete('/tasks/130')
        assert response.status_code == 404
        assert response.json['status'] == 'error'


def test_get_all_tasks():
    with app.test_client() as client:
        response = client.get('/tasks')
        assert response.status_code == 200
        assert type(response.json) is list
