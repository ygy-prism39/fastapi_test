import datetime
import asyncio
from typing   import List, Optional

from pydantic import BaseModel

async def some_function(user_id: str):
    await asyncio.sleep(3)
    return user_id

class User(BaseModel):
    id      : int
    name    : str
    joined  : Optional[datetime.datetime] = None
    friends : List[int] = []


user_data = {
    'id'      : 4,
    'name'    : 'testtwo',
    'joined'  : '2020-01-02 00:00',
    'friends' : [1, "2", b"3"],
}

my_user: User = User(**user_data)

print(my_user)
