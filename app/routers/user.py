from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from sqlalchemy import insert, update, delete, select
from slugify import slugify
from app.models.user import User
from app.schemas import CreateUser

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Session = Depends(get_db)):
    users = db.execute(select(User).where(User.is_active == True)).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )


@router.post("/create")
async def create_user(create_user: CreateUser, db: Session = Depends(get_db)):
    db.execute(insert(User).values(
        name=create_user.name,
        parent_id=create_user.parent_id,
        slug=slugify(create_user.name)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put("/update/user")
async def update_user(user_id: int, update_user: CreateUser, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalar()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    db.execute(update(User).where(User.id == user_id).values(
        username=update_user.username,
        firstname=update_user.firstname,
        lastname=update_user.lastname,
        age=update_user.age)
    )
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'User update is successful'
    }

@router.delete("/delete/user")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalar()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )
    db.execute(delete(User).where(User.id == user_id).values(is_active=False))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'User delete is successful'
    }
