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

class ItemUpdate(BaseModel):
    name: str | None = None
    price: float | None = None

class ItemListRespone(BaseModel):
    items: list[ItemPublic]
    total: int
    skip: int
    limit: int

def check_name_conflict(name: str, exclude_id: int = None):
    if not name:
        return
    name_lower = name.strip().lower()
    for item in items_db:
        if exclude_id and item.id == exclude_id:
            continue
        if item.name.strip().lower() == name_lower:
            raise HTTPException(status_code=400, detail="Item with this name already exists")

@app.post("/items", response_model=ItemPublic, status_code=201)
def create_item(data: ItemCreate):
    global next_id
    check_name_conflict(data.name)
    item = ItemPublic(id=next_id,name= data.name, price= data.price)
    items_db.append(item)
    next_id += 1
    return item

@app.get("/items", response_model= ItemListRespone)
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    min_price: float | None = None,
    max_price: float | None = None,
    q: str | None = Query(None,min_length=2),
    sort_by: str = Query("id", pattern = "^(id|name|price)$"),
    order: str = Query("asc", pattern = "^(asc|desc)$")
):

    result = items_db.copy()

    if min_price is not None:
        result = [item for item in result if item.price >= min_price]
    if max_price is not None:
        result = [item for item in result if item.price <= max_price]

    if q is not None:
        result = [item for item in result if q.lower() in item.name.lower()]

    is_reverse = True if order == "desc" else False

    if sort_by == "price":
        result.sort(key=lambda x: x.price, reverse=is_reverse)
    elif sort_by == "name":
        result.sort(key=lambda x: x.name.lower(), reverse=is_reverse)
    else:
        result.sort(key=lambda x: x.id, reverse=is_reverse)

    total_count = len(result)

    paginated_items =  result[skip:skip + limit]

    return {
        "items": paginated_items,
        "total": total_count,
        "skip": skip,
        "limit": limit
    }

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
    check_name_conflict(data.name, exclude_id= item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = data.name
    item.price = data.price
    return item

@app.patch("/items/{item_id}", response_model=ItemPublic)
def patch_item(item_id: int, data: ItemUpdate):
    item = find_item(item_id)
    update_data = data.model_dump(exclude_unset=True)
    if "name" in update_data:
        check_name_conflict(update_data["name"], exclude_id = item_id)
        item.name = update_data["name"]
    if "price" in update_data:
        item.price = update_data["price"]

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