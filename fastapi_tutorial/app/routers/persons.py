from fastapi        import APIRouter, Depends

from sqlalchemy.orm import Session

from ..             import database, schemas
from ..repositories import persons

router = APIRouter(
    prefix = "/person",
    tags   = ["Persons"]
)
get_db = database.get_db


@router.post('/person', response_model=schemas.PersonOut)
def create_person(request: schemas.PersonIn, db: Session = Depends(get_db)):
    return persons.create_person(request, db)

@router.get('/person/{id}', response_model=schemas.PersonOut)
def get_person(id: int, db: Session = Depends(get_db)):
   return persons.get_person(id, db)

