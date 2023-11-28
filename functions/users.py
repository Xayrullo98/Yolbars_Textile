from fastapi import HTTPException
from sqlalchemy.orm import joinedload


from routes.login import get_password_hash
from utils.db_operations import the_one, the_one_username
from utils.pagination import pagination
from models.users import Users


def all_users(search, role, page, limit, status, db):
    users = db.query(Users)
    if search:
        search_formatted = "%{}%".format(search)
        users = users.filter(Users.name.like(search_formatted) | Users.username.like(search_formatted)
                            )

    if status in [True, False]:
        users = users.filter(Users.status == status)
    if role:
        users = users.filter(Users.role == role)
    users = users.order_by(Users.id.desc())
    return pagination(users, page, limit)


def create_user(form, db, thisuser):
    the_one_username(db=db, model=Users, username=form.username)
    if thisuser.role != 'admin':
        raise HTTPException(status_code=400, detail="Sizga ruhsat berilmagan")
    if form.role not in ['admin', 'stage_admin', 'stage_user', 'warehouseman']:
        raise HTTPException(status_code=400, detail="Role error")
    new_user_db = Users(
        name=form.name,
        username=form.username,
        status=True,
        role=form.role,
        password=get_password_hash(form.password),
        phone=form.phone,
    )
    db.add(new_user_db)
    db.flush()

    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def one_user(db, id):
    the_item = db.query(Users).filter(Users.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday user mavjud emas")


def update_user(form, thisuser, db):
    user = the_one(db=db, model=Users, id=form.id)
    if form.role not in ['admin', 'stage_admin', 'stage_user', 'warehouseman']:
        raise HTTPException(status_code=400, detail="Role error")
    if db.query(Users).filter(Users.username == form.username).first() and user.username != form.username:
        raise HTTPException(status_code=400, detail="Bu username bazada mavjud")


    db.query(Users).filter(Users.id == form.id).update({
            Users.name: form.name,
            Users.username: form.username,
            Users.password: get_password_hash(form.password),
            Users.phone: form.phone,
            Users.status: form.status,
            Users.role: form.role,
        })


    db.commit()


