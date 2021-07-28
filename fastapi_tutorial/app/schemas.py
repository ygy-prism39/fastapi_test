from typing   import Optional, List, Set
from enum     import Enum
from datetime import datetime, time, timedelta
from uuid     import UUID

from pydantic import BaseModel, Field, HttpUrl, EmailStr


class PersonBase(BaseModel):
    name  : str
    email : str
    class Config():
        orm_mode = True

class BlogBase(BaseModel):
    title : str
    body  : str
    class Config():
        orm_mode = True

class PersonOut(PersonBase):
    blogs : List[BlogBase] = []

class PersonIn(PersonBase):
    password : str

class BlogOut(BlogBase):
    creator : PersonBase

class BlogIn(BlogBase):
    owner_id : int


class Login(BaseModel):
    email    : str
    password : str

class Token(BaseModel):
    access_token : str
    token_type   : str

class TokenData(BaseModel):
    email : Optional[str] = None


###############

class Item(BaseModel):
    name     : str
    price    : float
    is_offer : Optional[bool] = None

# predefined를 위해 Enum을 사용
class ModelName(str, Enum):  # str을 상속해야 type을 string으로 고정
    alexnet = "alexnet"
    resnet  = "resnet"
    lenet   = "lenet"

# Submodel
class Image(BaseModel):
    url  : HttpUrl
    name : str

# Field를 이용한 모델 생성
class User(BaseModel):
    name        : str
    description : Optional[str]   = Field(None, title="title", max_length=300)
    weight      : float           = Field(..., gt=0, description="weight must be positive")
    tags        : List[str]       = []
    tags2       : Set[str]        = set()
    images      : Optional[List[Image]] = None
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2,
#     "tags": ["rock", "metal", "bar"],
#     "images": [
#         {
#         "url": "http://example.com/baz.jpg",
#         "name": "The Foo live"
#         },
#         ...
#     ]
# }

# 이외 특이한 type
class Process(BaseModel):
    item_id        : UUID
    start_datetime : Optional[datetime]  = Field(None)
    repeat_at      : Optional[time]      = Field(None)
    process_after  : Optional[timedelta] = Field(None)

# model의 상속을 이용해서 중복 제거
class UserOut(BaseModel):
    username  : str
    email     : EmailStr
    full_name : Optional[str] = None
class UserIn(UserOut):
    password : str
class UserInDB(UserOut):
    hashed_password: str

# user 정보 저장 관련 참고
def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password
def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


