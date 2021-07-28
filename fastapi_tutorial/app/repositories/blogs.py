from fastapi        import HTTPException, status, Response

from sqlalchemy.orm import Session

from ..             import schemas
from ..models       import Person, Blog


def get_all(db: Session, current_user: schemas.TokenData):
    return db.query(Blog).join(Person).filter(Person.email == current_user.email).all()

def create(request: schemas.BlogIn, db: Session):
    blog = Blog(title=request.title, body=request.body, owner_id=request.owner_id)

    db.add(blog)
    db.commit()
    db.refresh(blog)

    return blog

def get_one(blog_id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id==blog_id).first()
    
    if not blog:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail      = f"id {blog_id} is not available"
        )

    return blog

def delete_one(blog_id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id==blog_id)

    if not blog.first():
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = f"id {blog_id} is not available"
        )

    blog.delete(synchronize_session=False)
    db.commit()

    # 204의 경우 message body가 있을 수 없기 때문에 Response object를 리턴해야 한다.
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def update_one(blog_id: int, request: schemas.BlogIn, db: Session):
    blog = db.query(Blog).filter(Blog.id==blog_id)
    
    if not blog.first():
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = f"id {blog_id} is not available"
        )

    blog.update(request.dict())
    db.commit()
    
    return 'updated'
