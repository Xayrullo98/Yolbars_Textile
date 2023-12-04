import inspect
import os
import shutil

from fastapi import APIRouter, HTTPException, Depends, Body, UploadFile, File
from sqlalchemy.orm import Session
from functions.category_items import create_category_item, update_category_item, all_category_items, one_category_item
import typing

from functions.uploaded_files import create_uploaded_file, one_uploaded_file_via_source, file_delete
from routes.login import get_current_active_user
from utils.role_verification import role_verification
from schemes.category_items import CreateCategories,UpdateCategories
from db import database
from schemes.users import UserCurrent
category_items_router = APIRouter(
    prefix="/category_items",
    tags=["Category items operation"]
)

"""
id: int = Body ( ..., ge=0 ),
            comment: typing.Optional[str] = Body ( '' ),
            source: typing.Optional[str] = Body ( '' ),
            files: typing.Optional[List[UploadFile]] = File ( None ), db: Session = Depends ( get_db ),
            current_user: UserCurrent = Depends ( get_current_active_user )):
    order=one_order ( id=id, db=db )
    order_status = status_dict.get(source)
    user=one_user ( id=current_user.id, db=db )

    if source == 'created':
        db.query ( Orders ).filter ( Orders.id == id ).update ( {
            Orders.id: id,
            Orders.user_id: user.id,
            Orders.order_status: order_status,
            Orders.updated_day: datetime.datetime.now ( ).date ( ),
            Orders.created_date: datetime.datetime.now ( ).date ( )} )
        db.commit ( )
        if files:
            for file in files:
                with open ( "media/" + file.filename, 'wb' ) as image:
                    shutil.copyfileobj ( file.file, image )
                url=str ( 'media/' + file.filename )
                create_uploaded_file ( source_id=id, source=source, file_url=url, comment=comment,
                                       user=current_user, db=db )


"""
@category_items_router.post('/add', )
def add_category_items(text: typing.Optional[str] = Body ( '' ),
                       category_id:int = Body ( '' ),
                       comment: typing.Optional[str] = Body ( '' ),
                       files: typing.Optional[UploadFile] = File (None), db: Session = Depends(database),
                       current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)

    response = create_category_item(text=text,category_id=category_id, db=db, thisuser=current_user)
    if files:
        # for file in files:
            with open("media/" + files.filename, 'wb') as image:
                shutil.copyfileobj(files.file, image)
            url = str('media/' + files.filename)
            create_uploaded_file(source_id=response.get('id'), source="category_item", file_url=url, comment=comment,
                                 user=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


@category_items_router.get('/', status_code=200)
def get_category_items(search: str = None,  id: int = 0, page: int = 1,
              limit: int = 25, status: bool = None, db: Session = Depends(database),
              ):

    if id:
        return one_category_item(db, id)
    else:
        # role_verification(current_user, inspect.currentframe().f_code.co_name)
        return all_category_items(search=search,  page=page, limit=limit, status=status, db=db, )


@category_items_router.put("/update")
def category_items_update(text: typing.Optional[str] = Body ( '' ),
                       id:int = Body ( '' ),
                       category_id:int = Body ( '' ),
                       comment: typing.Optional[str] = Body ( '' ),
                       files: typing.Optional[UploadFile] = File (None), db: Session = Depends(database),
                current_user: UserCurrent = Depends(get_current_active_user)):

    role_verification(current_user, inspect.currentframe().f_code.co_name)
    update_category_item(id=id,text=text,category_id=category_id,thisuser= current_user, db=db)
    old_files = one_uploaded_file_via_source(source_id=id, source="category_item", db=db)
    for file in old_files:
        try:
            os.unlink(file.file)
            file_delete(id=file.id, cur_user=current_user, db=db)

        except Exception as a:
                pass
    if files:
        # for file in files:
            with open("media/" + files.filename, 'wb') as image:
                shutil.copyfileobj(files.file, image)
            url = str('media/' + files.filename)
            create_uploaded_file(source_id=id, source="category_item", file_url=url, comment=comment,
                                 user=current_user, db=db)
    raise HTTPException(status_code=200, detail="Amaliyot muvaffaqiyatli amalga oshirildi")


