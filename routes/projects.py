import inspect
import os
import shutil
import typing

from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Body
from sqlalchemy.orm import Session
from functions.projects import create_project, update_project, all_projects, one_project
from functions.uploaded_files import create_uploaded_file, uploaded_files_delete, one_uploaded_file_via_source, \
    file_delete

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
def projects_update(name: str = Body(...),
                 url: str = Body(...),
                 id: int = Body(...),
                 source_id: int = Body(...),
                 comment: typing.Optional[str] = Body(...),
                 files: typing.Optional[typing.List[UploadFile]] = File(None), db: Session = Depends(database),
                    current_user: UserCurrent = Depends(get_current_active_user)):
    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_project(name=name,id=id,comment=comment,url=url,source_id=source_id, thisuser=current_user, db=db)
    old_files = one_uploaded_file_via_source(source_id=id,source="project",db=db)
    for file in old_files:
        try:
            os.unlink(file.file)
            file_delete(id=file.id,cur_user=current_user,db=db)
            print(file.file,'ggggggggggggggggggggggggggg')
        except Exception as a :
            print(a,'fffffffffffffffffffff')
    if files:
        for file in files:
            with open("media/" + file.filename, 'wb') as image:
                shutil.copyfileobj(file.file, image)
            url = str('media/' + file.filename)
            create_uploaded_file(source_id=id, source="project", file_url=url, comment=comment,
                                 user=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")
