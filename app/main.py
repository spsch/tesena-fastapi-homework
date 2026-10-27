from typing import Dict, List
from fastapi import FastAPI, HTTPException, status
from app.schemas import Item, ItemCreate, ItemUpdate

app = FastAPI(
    title="tesena-fastapi-homework",
    description="A simple CRUD API for managing items",
    version="1.0.0"
)

# In-memory databáze
db: Dict[int, dict] = {}
id_counter: int = 1

def get_db():
    return db

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, summary="Create item")
def create_item(item: ItemCreate):
    global id_counter
    item_dict = item.model_dump()
    item_dict["id"] = id_counter
    db[id_counter] = item_dict
    id_counter += 1
    return item_dict

@app.get("/items/", response_model=List[Item], status_code=status.HTTP_200_OK, summary="List of items (Read All)")
def read_items():
    return list(db.values())

@app.get("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK, summary="Detail of item (Read One)")
def read_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]

@app.put("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK, summary="Update item")
def update_item(item_id: int, item_update: ItemUpdate):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    stored_item = db[item_id]
    update_data = item_update.model_dump(exclude_unset=True)
    stored_item.update(update_data)
    db[item_id] = stored_item
    return stored_item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete item")
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return None