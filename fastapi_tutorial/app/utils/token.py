from datetime      import datetime, timedelta

from jose          import jwt, JWTError

from ..            import schemas
from ..my_settings import SECRET


def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=SECRET['ACCESS_TOKEN_EXPIRE_MINUTES'])
    data.update({"exp": expire})
    return jwt.encode(data, SECRET['KEY'], algorithm=SECRET['ALGORITHM'])

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET["KEY"], algorithms=SECRET["ALGORITHM"])
        email = payload.get("user")
        if email is None:
            raise credentials_exception
        return schemas.TokenData(email = email)
    except JWTError:
        raise credentials_exception
