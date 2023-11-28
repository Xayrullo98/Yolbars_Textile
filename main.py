from fastapi import FastAPI
import datetime
from fastapi.middleware.cors import CORSMiddleware

from routes import users ,login,projects,category_items,categories,targets,uploaded_files

app = FastAPI()


from db import Base, engine
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


@app.get('/')
def home():
    return {"message": "Welcome"}


app.include_router(login.login_router)
app.include_router(users.users_router)
app.include_router(categories.categories_router)
app.include_router(projects.projects_router)
app.include_router(targets.targets_router)
app.include_router(category_items.category_items_router)
app.include_router(uploaded_files.uploaded_files_router)

# @app.on_event("startup")
# @repeat_every(seconds=86400, wait_first=True)
# async def check():
#     timee = datetime.datetime.now().strftime("%d") == "03"
#     if timee:

