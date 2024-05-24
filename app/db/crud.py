from datetime import datetime

from sqlalchemy import insert, select, update, delete

from app.db.database import async_session, Base


class SQLAlchemyRepository:
    def __init__(self, model):
        self.model = model

    async def create(self, data: dict):
        async with async_session() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            resp = await session.execute(stmt)
            await session.commit()
            return resp.scalars().all()

    async def find_by_id(self, task_id: int):
        async with async_session() as session:
            stmt = select(self.model).filter_by(id=task_id)
            resp = await session.execute(stmt)
            return resp.first()

    async def find_all(self):
        async with async_session() as session:
            stmt = select(self.model)
            resp = await session.execute(stmt)
            return resp.scalars().all()

    async def update_task(self, task_id: int, data: dict):
        async with async_session() as session:
            data.update(update_at=datetime.now())
            data = {result: data[result] for result in data if data[result] is not None}
            stmt = update(self.model).filter_by(id=task_id).values(**data).returning(self.model)
            resp = await session.execute(stmt)
            await session.commit()
            return resp.first()

    async def delete_task(self, task_id: int):
        async with async_session() as session:
            stmt = delete(self.model).filter_by(id=task_id).returning(self.model.id)
            resp = await session.execute(stmt)
            await session.commit()
            return resp.scalar()
