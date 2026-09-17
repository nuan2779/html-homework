from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

#LAB 1 & 2
items_db = []
next_id = 1

class ItemCreate(BaseModel):
    name: str
    price: float

class ItemPublic(BaseModel):
    id: int
    name: str
    price: float

@app.post("/items", response_model=ItemPublic, status_code=201)
def create_item(data: ItemCreate):
    global next_id
    item = ItemPublic(id=next_id,name= data.name, price= data.price)
    items_db.append(item)
    next_id += 1
    return item

@app.get("/items", response_model=list[ItemPublic])
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return items_db[skip:skip + limit]

def find_item(item_id:int):
    for item in items_db:
        if item.id == item_id:
            return item
    return None
@app.get("/items/{item_id}", response_model=ItemPublic)
def get_item(item_id: int):
    item = find_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=ItemPublic)
def update_item(item_id: int, data: ItemCreate):
    item = find_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = data.name
    item.price = data.price
    return item

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    item = find_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db.remove(item)
    return None

#LAB 3
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="../frontend"), name="static")