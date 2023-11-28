import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.targets import create_target, update_target, all_targets, one_target, add_visits

from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.targets import CreateTarget,UpdateTarget
from db import database
from schemes.users import UserCurrent
targets_router = APIRouter(
    prefix="/targets",
    tags=["Target operation"]
)


@targets_router.post('/add', )
def add_targets(form: CreateTarget, db: Session = Depends(database),
             current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    create_target(form=form, db=db, thisuser=current_user)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@targets_router.get('/', status_code=200)
def get_targets(search: str = None,  id: int = 0, page: int = 1,
              limit: int = 25, status: bool = None, db: Session = Depends(database),
              current_user: UserCurrent = Depends(get_current_active_user)):

    if id:
        return one_target(db, id)
    else:
        role_verification(current_user, inspect.currentframe().f_code.co_name)
        return all_targets(search=search,  page=page, limit=limit, status=status, db=db, )


@targets_router.get('/visit', status_code=200)
def get_targets(link: str = None, db: Session = Depends(database),
              ):
    add_visits(link=link,db=db)


@targets_router.put("/update")
def targets_update(form: UpdateTarget, db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_target(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


