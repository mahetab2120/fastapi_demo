from fastapi import Response,status,HTTPException,Depends,APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

from .. import models,utils,schemas

router = APIRouter(
    prefix="/users",
    tags=['User']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.userOut)
def test_post(user:schemas.userCreate,db:Session=Depends(get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    posts=models.User(**user.dict())
    #posts=models.Post(title=post.title,content=post.content,published=post.published)
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts

@router.get("/{id}",response_model=schemas.userOut)
def get_user(id:int,db:Session=Depends(get_db)):
    
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id : {id} does not exist")
    
    return user