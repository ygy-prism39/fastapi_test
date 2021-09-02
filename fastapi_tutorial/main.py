from typing           import Optional, List

from fastapi          import FastAPI, Query, Path, Body, Cookie, Header

from .app.some_module import some_function
from .app.schemas     import *

app = FastAPI()


##########
# 비동기 #
##########
@app.get("/")
async def read_root():
#    print(1)
#    results = await some_function('1')
#    print(2)
#    return results
    return "test"


################
# request body #
################
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, q: Optional[str] = None):
    return {"item_name": item.name, "item_id": item_id, "q": q, **item.dict()}

# model을 사용하지 않고 Body에 넣을 변수를 정하고 싶을 때는 Body()를 이용하자.
@app.post("/items/{item_id}")
async def post_item(
        item_id    : int,
        item       : Item,
        importance : int = Body(...)
):
    results = {"item_id": item_id, "item": item, "importance": importance}
    return results
# 위에서 기대하는 request.body
# {
#   "item": {
#     "name": "string",
#     "price": 0,
#     "is_offer": true
#   },
#   "importance": 0
# }

# Body(..., embed=True)를 이용하면
# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2
# }
# 대신
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     }
# } 이렇게


##################
# path parameter #
##################
# 순서대로
@app.get("/items/all")
def read_items():
    return []

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

# Predefined path parameters
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# path parameters including path URL
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

# @app.get("/users/{user_id}/items/{item_id}")와 같이 multipath도 가능

# Path()를 이용하면 Query와 Path가 섞여있어도 순서가 상관이 없다. 보기에도 명확함.
@app.get("/some_path/{item}")
async def read_item_by_path(
        item : int           = Path(..., title="title", ge=1, le=1000),
        q    : Optional[str] = Query(None)
):
    results = {"item": str(item)}
    if q:
        results.update({"q": q})
    return results
# ge와 le를 이용하면 input의 범위를 정해줄 수 있다.


###################
# query parameter #
###################
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/offset")
async def read_item_by_query(offset: int = 0, limit: int = 10):
    return fake_items_db[offset: offset+limit]

# query parameter optional
@app.get("/optional")
async def read_item_by_query_optional(q: Optional[str] = None):
    return {"q": q}

# query parameter type conversion
@app.get("/items/names/{item_name}")
async def read_item_by_query_bool(item_name: str, q: Optional[str] = None, short: bool = False):
    item = {"item_name": item_name}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# async def read_user_item(needy: str):와 같이 하면 needy query는 필수

# additional validation
@app.get("/validation")
async def read_items_by_query_additional(q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^asdf$")):
    results = {"items": "Foo"}
    if q:
        results.update({"q": q})
    return results

# Query(None, ) 에서 None자리가 default value가 오는 자리 (ex. q: str = Query("defaultquery", min_length=3))
# q: str = Query(..., min_length=3)으로 하면 q가 필수로 요구됨.

# query parameter list / multiple values
@app.get("/multiple_query")
async def read_items_multiple_query(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items

# query list에서 default 값 주기: async def read_items(q: List[str] = Query(["foo", "bar"])): 

# query의 keyword 값 바꾸기: async def read_items(q: Optional[str] = Query(None, alias="item-query")):


############################
# cookie, header parameter #
############################
@app.get("/cookies")
async def read_items_by_cookies(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}

@app.get("/headers")
async def read_items_by_headers(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}


##################
# response model #
##################
# response model을 사용하면 input받은 데이터를 그대로 return해도 실제로 response되는 데이터를 필터링 할 수 있다.
# status_code를 추가하여 response의 code 또한 지정할 수 있다.
@app.post("/response", response_model=UserOut, status_code=201)
async def create_user(user: UserIn):
    user_saved = fake_save_user(user)
    return user_saved

# JSON 대신 Form data, File data, UploadFile data 로도 주고받을 수 있다.
# file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
