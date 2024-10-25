from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from sqlalchemy import insert
from slugify import slugify

from app.models.task import Task
from app.models.user import User
from app.schemas import CreateTask
from sqlalchemy import update

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    task = db.skalars(select(Task).where(Task.is_active == True)).all()
    if task is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )


@router.post("/create")
async def create_task(create_user: CreateTask, db: Annotated[Session, Depends(get_db)], create_task=None):
    db.execute(insert(Task).values(name=create_task.name,
                                   parent_id=create_task.parent_id,
                                   description=create_user.description,
                                   slug=slugify(create_task.name)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


from sqlalchemy import select


@router.get('/{user.slug}')
async def user_by_task(db: Annotated[Session, Depends(get_db)], user_slug=str):
    user = db.scalar(select(User).where(User.slug == user_slug))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found"
        )

@router.put("/update")
async def update_task(update_user: CreateTask, db: Annotated[Session, Depends(get_db)], update_task=None):
    db.execute(insert(Task).values(name=update_task.name,
                                   parent_id=update_task.parent_id,
                                   description=update_user.description,
                                   slug=slugify(update_task.name)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }



@router.delete("/delete/task")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar()
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    db.execute(delete(Task).where(Task.id == task_id).values(is_active=False))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Task delete is successful'
    }
