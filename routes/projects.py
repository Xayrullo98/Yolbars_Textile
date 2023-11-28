import inspect
import shutil
import typing

from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Body
from sqlalchemy.orm import Session
from functions.projects import create_project, update_project, all_projects, one_project
from functions.uploaded_files import create_uploaded_file

from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.projects import CreateProject, UpdateProject
from db import database
from schemes.users import UserCurrent

projects_router = APIRouter(
    prefix="/projects",
    tags=["Projects operation"]
)


@projects_router.post('/add', )
def add_projects(name: str = Body(''),
                 url: str = Body(''),
                 source_id: int = Body(''),
                 comment: typing.Optional[str] = Body(''),
                 files: typing.Optional[typing.List[UploadFile]] = File(None), db: Session = Depends(database),
                 current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    response = create_project(name=name,url=url,source_id=source_id,comment=comment, db=db, thisuser=current_user)
    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            create_uploaded_file(source_id=response.get('id'), source="project", file_url=url, comment=comment,
                                 user=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@projects_router.get('/', status_code=200)
def get_projects(search: str = None, id: int = 0, page: int = 1,
                 limit: int = 25, status: bool = None, db: Session = Depends(database),
                 ):
    if id:
        return one_project(db, id)
    else:
        # role_verification(current_user, inspect.currentframe().f_code.co_name)
        return all_projects(search=search, page=page, limit=limit, status=status, db=db, )


@projects_router.put("/update")
def projects_update(form: UpdateProject, db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_project(form, current_user, db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
