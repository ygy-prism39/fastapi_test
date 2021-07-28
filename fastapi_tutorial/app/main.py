from fastapi  import FastAPI

from .routers import blogs, persons, authentication 
from .        import database, models


app = FastAPI()
models.Base.metadata.create_all(database.engine)

app.include_router(blogs.router)
app.include_router(persons.router)
app.include_router(authentication.router)
