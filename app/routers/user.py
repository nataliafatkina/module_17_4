from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import User, Task
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User was not found')


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], creating_user: CreateUser):
    db.execute(insert(User).values(username=creating_user.username,
                                   firstname=creating_user.firstname,
                                   lastname=creating_user.lastname,
                                   age=creating_user.age,
                                   slug=slugify(creating_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)], updating_user: UpdateUser, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        db.execute(update(User).where(User.id == user_id).values(firstname=updating_user.firstname,
                                   lastname=updating_user.lastname,
                                   age=updating_user.age))
        db.commit()
        return {'status_code': status.HTTP_200_OK,
                'transaction': 'User update is successful!'}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='User was not found')


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        db.execute(delete(User).where(User.id == user_id))
        db.execute(delete(Task).where(Task.user_id == user_id))
        db.commit()
        return {'status_code': status.HTTP_200_OK,
                'transaction': 'User delete is successful!'}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail='User was not found')
