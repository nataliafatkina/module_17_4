from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is not None:
        return task
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Task was not found')

@router.get('/user_id/tasks')
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    tasks_by_user = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    return tasks_by_user


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], creating_task: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        db.execute(insert(Task).values(title=creating_task.title,
                                       content=creating_task.content,
                                       priority=creating_task.priority,
                                       user_id=user_id,
                                       slug=slugify(creating_task.title)))
        db.commit()
        return {'status_code': status.HTTP_201_CREATED,
                'transaction': 'Successful'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='User was not found')


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)], updating_task: UpdateTask, task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is not None:
        db.execute(update(Task).where(Task.id == task_id).values(title=updating_task.title,
                                   content=updating_task.content,
                                   priority=updating_task.priority))
        db.commit()
        return {'status_code': status.HTTP_200_OK,
                'transaction': 'Task update is successful!'}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Task was not found')


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is not None:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK,
                'transaction': 'Task delete is successful!'}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='Task was not found')
