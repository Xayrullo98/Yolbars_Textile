import inspect
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from functions.statistics import order_statistics
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from db import database
from utils.db_operations import the_one
from schemes.users import UserCurrent
from datetime import date
statistics_router = APIRouter(
    prefix="/statistics",
    tags=["Statistics operation"]
)


@statistics_router.get('/', status_code=200)
def get_order_statistics(order_id: int = 0, from_time: date = None, to_time: date = None, page: int = 1, limit: int = 25, db: Session = Depends(database), current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    return order_statistics(order_id, from_time, to_time, page, limit, db)