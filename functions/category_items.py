from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.categories import Categories
from utils.db_operations import the_one
from utils.pagination import pagination
from models.category_items import Category_items


def all_category_items(search,  page, limit, status, db):
    category_items = db.query(Category_items).options(joinedload(Category_items.category),joinedload(Category_items.category_item_files))
    if search:
        search_formatted = "%{}%".format(search)
        category_items = category_items.filter(
            Category_items.text.like(search_formatted)
            )
    if status in [True, False]:
        category_items = category_items.filter(Category_items.status == status)

    category_items = category_items.order_by(Category_items.id.desc())
    return pagination(category_items, page, limit)


def create_category_item(text,category_id, db, thisuser):
    the_one(id=category_id,model=Categories,db=db)
    new_user_db = Category_items(
        text=text,
        category_id=category_id,
        user_id=thisuser.id,
    )
    db.add(new_user_db)
    db.flush()
    db.commit()
    return {"id":new_user_db.id}


def one_category_item(db, id):
    the_item = db.query(Category_items).options(joinedload(Category_items.category)).filter(Category_items.id==id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday user mavjud emas")


def update_category_item(form, thisuser, db):
    the_one(id=form.category_id, model=Categories, db=db)
    the_one(id=form.id, model=Category_items, db=db)
    db.query(Category_items).filter(Category_items.id == form.id).update({
        Category_items.text: form.text,
        Category_items.category_id: form.category_id,
        Category_items.status: form.status,
    })

    db.commit()
