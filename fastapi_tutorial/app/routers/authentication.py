from fastapi          import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm   import Session

from ..               import database, models
from ..utils          import hashing, token

router = APIRouter(tags=['authentication'])
get_db = database.get_db


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Person).filter(models.Person.email == request.username).first()

    if not user:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail      = "invalid_email"
        )

    if not hashing.Hash.verify(request.password, user.password):
         raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail      = "invalid_password"
        )

    data = {"user": user.email}
    access_token = token.create_access_token(data)

    return {"access_token": access_token, "token_type": "bearer"}
