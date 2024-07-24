from typing import List

from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from app import models, oauth2, schemas
from app.database import get_db

from datetime import datetime, timedelta

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)


@router.get("/", response_model=List[schemas.Task])
def get_tasks(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    tasks = db.query(models.Task).filter(models.Task.owner == current_user, models.Task.isCompleted == False).all()
    return tasks


@router.get("/{id}", response_model=schemas.Task)
async def get_task(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    task = db.query(models.Task).filter(models.Task.owner == current_user, models.Task.id == id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task with id: {id} does not exist")
    return task


@router.get("/important/tasks", response_model=List[schemas.Task])
async def get_important_tasks(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    important_tasks = db.query(models.Task).filter(models.Task.owner == current_user,
                                                   models.Task.isImportant == True,
                                                   models.Task.isCompleted == False).all()
    return important_tasks


@router.get("/completed/tasks", response_model=List[schemas.Task])
async def get_completed_tasks(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    completed_tasks = db.query(models.Task).filter(models.Task.owner == current_user,
                                                   models.Task.isCompleted == True).all()
    return completed_tasks


@router.get("/do-it-now/tasks", response_model=List[schemas.Task])
async def get_do_it_now_tasks(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    now = datetime.utcnow()
    fourdayslater = now + timedelta(days=4)
    do_it_now_tasks = db.query(models.Task).filter(models.Task.owner == current_user,
                                                   models.Task.isCompleted == False,
                                                   models.Task.date < fourdayslater).all()

    return do_it_now_tasks


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.TaskCreate)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    new_task = models.Task(owner_id=current_user.id, **task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.put("/{id}", response_model=schemas.Task)
async def update_task(id: int, updated_task: schemas.Task, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    task_query = db.query(models.Task).filter(models.Task.owner == current_user, models.Task.id == id)
    task = task_query.first()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id: {id} does not exist")

    task_query.update(updated_task.dict(), synchronize_session=False)
    db.commit()

    return task_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    task_query = db.query(models.Task).filter(models.Task.owner == current_user, models.Task.id == id)
    task = task_query.first()

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Task with id: {id} does not exist")

    task_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)