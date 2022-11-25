
from enum import auto
import imp
from logging import exception
from typing import List
from sqlite3 import Cursor
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models,schemas,utils
from .database import engine,get_db
from sqlalchemy.orm import Session
from .routers import user,post,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_password)

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins=["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# try:
#     conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='2120',cursor_factory=RealDictCursor)
#     Cursor=conn.cursor()
#     print('connection successful')
# except Exception as error:
#     print('connecting to database faild',error)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World111"}



@app.get("/posts")
def get_posts():
    Cursor.execute('''SELECT * FROM pyapi''')
    post = Cursor.fetchall()
    print(post)
    return {"message": post}

# @app.post("/createposts")
# def create_posts(payload : dict=Body(...)):
#     print(payload)
#     return {"message": f"title:{payload['title']} , containt:{payload['post']}"}
# @app.post("/posts")
# def create_posts(new_post:schemas.CreatePost):
#     Cursor.execute('''INSERT INTO pyapi(title,content,published) VALUES(%s,%s,%s) RETURNING *''',(new_post.title,new_post.content,new_post.published))
#     post=Cursor.fetchone()
#     conn.commit()
#     return post

# @app.get("/posts/{id}")
# def create_posts(id:int):
#     Cursor.execute('''SELECT * FROM pyapi WHERE id=%s''',(str(id)))
#     post=Cursor.fetchone()
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id:{id} does not exist')
#     return {"data":post}

# @app.delete("/posts/{id}")
# def detele_posts(id:int):
#     Cursor.execute('''DELETE FROM pyapi WHERE id=%s RETURNING *''',(str(id)))
#     post=Cursor.fetchone()
#     conn.commit()
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id:{id} does not exist')
#     return {"data":post}

# @app.put("/posts/{id}")
# def update_posts(id:int,post:schemas.CreatePost):
#     Cursor.execute('''UPDATE pyapi SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *''',(post.title,post.content,post.publish,str(id)))
#     post=Cursor.fetchone()
#     conn.commit()
#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id:{id} does not exist')
#     return {"data":post}

