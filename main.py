import typing
import fastapi

app = fastapi.FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: typing.Union[str, None] = None):
    return {"item_id": item_id, "q": q}
