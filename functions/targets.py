from fastapi import HTTPException
from sqlalchemy.orm import joinedload
import uuid
from models.projects import Projects
from utils.db_operations import the_one
from utils.pagination import pagination
from models.targets import Targets


def all_targets(search, page, limit, status, db):
    targets = db.query(Targets).options(joinedload(Targets.project))
    if search:
        search_formatted = "%{}%".format(search)
        targets = targets.filter(
            Targets.name.like(search_formatted)
        )

    if status in [True, False]:
        targets = targets.filter(Targets.status == status)

    targets = targets.order_by(Targets.id.desc())
    return pagination(targets, page, limit)


def create_target(form, db, thisuser):
    the_one(id=form.project_id, model=Projects, db=db)
    if form.link[-1] == '/':
        link = str(form.link) + str(uuid.uuid4())
    else:
        link = str(form.link) + '/' + str(uuid.uuid4())
    new_user_db = Targets(
        link=link,
        comment=form.comment,
        project_id=form.project_id,
        watches=0,
        user_id=thisuser.id,
    )
    db.add(new_user_db)
    db.flush()

    db.commit()
    raise HTTPException(status_code=200, detail=f"Amaliyot muvaffaqiyatli bajarildi")


def one_target(db, id):
    the_item = db.query(Targets).options(joinedload(Targets.project)).filter(Targets.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday user mavjud emas")


def update_target(form, thisuser, db):
    the_one(id=form.project_id, model=Projects, db=db)

    db.query(Targets).filter(Targets.id == form.id).update({
        Targets.link: form.link,
        Targets.comment: form.comment,
        Targets.project_id: form.project_id,
        Targets.status: form.status,
    })

    db.commit()


def add_visits(link, db):
    target = db.query(Targets).filter(Targets.link == link).first()
    new_number = target.watches + 1
    db.query(Targets).filter(Targets.link == link).update({
        Targets.watches: new_number
    })
    db.commit()
