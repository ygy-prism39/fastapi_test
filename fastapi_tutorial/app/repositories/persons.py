from fastapi        import HTTPException, status
from sqlalchemy.orm import Session

from ..             import models, schemas
from ..utils        import hashing


def create_person(request: schemas.PersonIn, db: Session):
    new_person = models.Person(name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password))

    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    return new_person

def get_person(id: int, db: Session):
    user = db.query(models.Person).filter(models.Person.id == id).first()

    if not user:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = f"id {id} is not available"
        )

    return user

