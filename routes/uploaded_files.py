import inspect
import shutil
import typing

from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Body
from sqlalchemy.orm import Session
from functions.uploaded_files import create_uploaded_file, update_uploaded_files, all_uploaded_filess, \
    one_uploaded_files, uploaded_files_delete
from functions.uploaded_files import create_uploaded_file

from routes.login import get_current_active_user
from utils.role_verification import role_verification
from db import database
from schemes.users import UserCurrent

uploaded_files_router = APIRouter(
    prefix="/uploaded_files",
    tags=["uploaded_files operation"]
)


@uploaded_files_router.post('/add', )
def add_uploaded_files(
        source_id: int = Body(''),
        source: str = Body(''),
        comment: typing.Optional[str] = Body(''),
        files: typing.Optional[UploadFile] = File(None), db: Session = Depends(database),
        current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    if files:
        # for file in files:
            with open("media/" + files.filename, 'wb') as image:
                shutil.copyfileobj(files.file, image)
            url = str('media/' + files.filename)
            create_uploaded_file(source_id=source_id, source=source, file_url=url, comment=comment,
                                 user=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@uploaded_files_router.get('/', status_code=200)
def get_uploaded_files(search: str = None, id: int = 0, source: str = None, source_id: int = 0, page: int = 1,
                       limit: int = 25, status: bool = None, db: Session = Depends(database),
                       ):
    if id:
        return one_uploaded_files(db, id)
    else:

        return all_uploaded_filess(search=search, source=source, source_id=source_id, page=page, limit=limit,
                                   status=status, db=db, )


@uploaded_files_router.delete("/delete")
def uploaded_files_updateid(id: int = 0, db: Session = Depends(database),
                            current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    uploaded_files_delete(id, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
