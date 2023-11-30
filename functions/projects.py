from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from models.categories import Categories
from utils.db_operations import the_one
from utils.pagination import pagination
from models.projects import Projects


def all_projects(search, page, limit, status, db):
    projects = db.query(Projects).options(joinedload(Projects.source),joinedload(Projects.project_files))
    if search:
        search_formatted = "%{}%".format(search)
        projects = projects.filter(
            Projects.name.like(search_formatted)
        )

    if status in [True, False]:
        projects = projects.filter(Projects.status == status)

    projects = projects.order_by(Projects.id.desc())
    return pagination(projects, page, limit)


def create_project(name,comment,url,source_id, db, thisuser):
    new_user_db = Projects(
        name=name,
        comment=comment,
        url=url,
        source_id=source_id,
        user_id=thisuser.id,
    )
    db.add(new_user_db)
    db.flush()

    db.commit()
    return {"id":new_user_db.id}

def one_project(db, id):
    the_item = db.query(Projects).options(joinedload(Projects.source)).filter(Projects.id == id).first()
    if the_item:
        return the_item
    raise HTTPException(status_code=400, detail="bunday user mavjud emas")


def update_project(id,name,comment,url,source_id, thisuser, db):
    the_one(db=db, model=Projects, id=id)
    the_one(db=db, model=Categories, id=source_id)

    db.query(Projects).filter(Projects.id == id).update({
        Projects.name: name,
        Projects.comment: comment,
        Projects.url: url,
        Projects.source_id: source_id,
     })

    db.commit()
