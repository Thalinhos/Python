from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


inventory = {
    1: {
        "name": "milk",
        "price": 3.99
    },
    2: {
        "name": "chocolate",
        "price": 2.99
    }
}

@app.get("/")
def get_item():
    return inventory

@app.get("/get_id/")
def get_item_id(item_id: int):
    if item_id in inventory:
        return inventory[item_id]
    return {"Data": "item not found"}

@app.get("/get-by-name")
def get_item(name: str):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Data": "No such item"}

@app.post("/create-item")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"Error": "Item_id already exists"}
    inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
    return inventory[item_id]

@app.put("/updateitem/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"error": "not in inventory"}
    
    if item.name != None:
        inventory[item_id]["name"] = item.name
    if item.price != None:
        inventory[item_id]["price"] = item.price
    if item.brand != None:
        inventory[item_id]["brandy"] = item.brand
    return inventory[item_id]


# @app.delete("/deleteitem") query method
# def delete_item(item_id: int):
#     if item_id not in inventory:
#         return {"Data": "item not exists"}
#     del inventory[item_id]

@app.delete("/deleteitem/{item_id}") #url method
def delete_item(item_id: int):
    if item_id not in inventory:
        return {"Data": "item not exists"}
    del inventory[item_id]