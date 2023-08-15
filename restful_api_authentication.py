from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Dummy data for demonstration purposes
class Item(BaseModel):
    name: str
    description: str

# Dummy database
db = []

# Bearer token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authentication function
def authenticate(token: str = Depends(oauth2_scheme)):
    if token != "mysecrettoken":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return token

@app.post("/token")
def login_for_access_token():
    return {"access_token": "mysecrettoken", "token_type": "bearer"}

@app.post("/items/", response_model=Item)
def create_item(item: Item, token: str = Depends(authenticate)):
    db.append(item)
    return item

@app.get("/items/", response_model=List[Item])
def read_items(token: str = Depends(authenticate)):
    return db

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, token: str = Depends(authenticate)):
    if 0 <= item_id < len(db):
        return db[item_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item, token: str = Depends(authenticate)):
    if 0 <= item_id < len(db):
        db[item_id] = item
        return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int, token: str = Depends(authenticate)):
    if 0 <= item_id < len(db):
        deleted_item = db.pop(item_id)
        return deleted_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
