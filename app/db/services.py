from flask import abort

from app.db.crud import SQLAlchemyRepository
from app.db.models import Tasks
from app.schemas.task import STaskAdd


class TaskService:
    def __init__(self):
        self.task_repo = SQLAlchemyRepository(model=Tasks)

    async def add_one(self, data: dict) -> dict:
        resp = await self.task_repo.create(data=data)
        # return {'fdgh': 'dgdf'}
        task = [STaskAdd.model_validate(result, from_attributes=True) for result in resp]
        return task[0].model_dump()

    async def find_one(self, task_id: int) -> dict:
        resp = await self.task_repo.find_by_id(task_id=task_id)
        if not resp:
            abort(404)
        task = [STaskAdd.model_validate(result, from_attributes=True) for result in resp]
        return task[0].model_dump()

    async def find_all(self) -> list[dict]:
        tasks = await self.task_repo.find_all()
        tasks_list = [STaskAdd.model_validate(result, from_attributes=True) for result in tasks]
        tasks_dict = [task.model_dump() for task in tasks_list]
        return tasks_dict

    async def update(self, task_id: int, data: dict) -> dict:
        resp = await self.task_repo.update_task(task_id=task_id, data=data)
        if not resp:
            abort(404)
        task = [STaskAdd.model_validate(result, from_attributes=True) for result in resp]
        return task[0].model_dump()

    async def delete(self, task_id):
        resp = await self.task_repo.delete_task(task_id=task_id)
        if not resp:
            abort(404)
        return resp
