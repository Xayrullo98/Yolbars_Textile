from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from utils.db_operations import the_one, the_one_username
from utils.pagination import pagination
from models.categories import Categories


def all_categories(search,  page, limit, status, db):
    categories = db.query(Categories)
    if search:
        search_formatted = "%{}%".format(search)
        categories = categories.filter(
            Categories.name.like(search_formatted) | Categories.comment.like(search_formatted)
            )

    if status in [True, False]:
        categories = categories.filter(Categories.status == status)

    categories = categories.order_by(Categories.id.desc())
    return pagination(categories, page, limit)


def create_category(form, db, thisuser):
    new_user_db = Categories(
        name=form.name,
        comment=form.comment,
        status=True,
        user_id=thisuser.id,
    )
    db.add(new_user_db)
    db.flush()

    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def one_category(db, id):
    the_item = db.query(Categories).filter(Categories.id==id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday user mavjud emas")


def update_category(form, thisuser, db):
    the_one(db=db, model=Categories, id=form.id)

    db.query(Categories).filter(Categories.id == form.id).update({
        Categories.name: form.name,
        Categories.status: form.status,
        Categories.comment: form.comment,
    })

    db.commit()
