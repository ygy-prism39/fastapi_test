from typing         import List

from fastapi        import APIRouter, status, Depends
from sqlalchemy.orm import Session

from ..             import schemas, database
from ..repositories import blogs
from ..utils        import oauth2

router = APIRouter(
        prefix = "/blog",
        tags   = ["blogs"]
)
get_db = database.get_db


@router.get('', response_model=List[schemas.BlogOut])
def get_all(db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    return blogs.get_all(db, current_user)

@router.post('', status_code= status.HTTP_201_CREATED, response_model=schemas.BlogOut)
def create(request: schemas.BlogIn, db: Session = Depends(get_db)):
    return blogs.create(request, db)

@router.get('/{blog_id}', response_model=schemas.BlogOut)
def get_one(blog_id: int, db: Session = Depends(get_db)):
    return blogs.get_one(blog_id, db)

@router.delete('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_one(blog_id: int, db: Session = Depends(get_db)):
    return blogs.delete_one(blog_id, db)

@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_one(blog_id: int, request: schemas.BlogIn, db: Session = Depends(get_db)):
    return blogs.update_one(blog_id, request, db)
