from fastapi import Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models,schemas,oauth2

router = APIRouter(
    prefix="/sqlalchemy",
    tags=['Post']
)


@router.get("/",response_model=List[schemas.PostOut])
def test_post(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
    print(current_user.id)
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts=db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def test_post(post:schemas.CreatePost,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    print(current_user.id)
    posts=models.Post(owner_id=current_user.id,**post.dict())
    #posts=models.Post(title=post.title,content=post.content,published=post.published)
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts

@router.get("/{id}")
def test_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    posts=db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    #db.query(models.Post).filter(models.Post.id==id).first()
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id:{id} does not exist')
    return{"data":posts}

@router.delete("/{id}")
def test_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    posts_query = db.query(models.Post).filter(models.Post.id==id)
    posts = posts_query.first()
    print(posts.id)
    if posts == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id:{id} does not exist')
    if posts.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Not authorized to perform requested action')
    posts_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def test_post(post:schemas.CreatePost,id:int,db:Session=Depends(get_db)):
    posts=db.query(models.Post).filter(models.Post.id==id)
    if posts.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id:{id} does not exist')
    posts.update(post.dict(),synchronize_Session=False)
    db.commit()
    return posts.first()