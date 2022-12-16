from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pymongo
from pymongo import MongoClient
from typing import Optional,List
import json

mongostr = "mongodb://localhost:27017"
client = MongoClient(mongostr)
db = client['Todo']
col = db['TodoList']

class Todo(BaseModel):
    _id:int
    name: str
    due_date: str
    desc: str

app = FastAPI(title="Todo API Assignment")

def docEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "name":item["name"],
        "due_date":item["due_date"],
        "desc":item["desc"]
    }

def docsEntity(entity) -> list:
    return [docEntity(item) for item in entity]

#returns test home page of the app
@app.get('/')
async def home():
    return {"Assignment":"Home"}

#creates and inserts a todo dictionary into the mongodb database
#(Must incclude all the fields from the Class todo in the parameters)
@app.post('/todo/')
async def create_todo(todo: Todo):
    col.insert_one(todo)
    return docEntity(todo)


#Returns All the documents present in the database
@app.get('/todo',response_model=List[Todo])
async def get_all_todos():
    lst = []
    for x in col.find():
        lst.append(x)
    return lst

#Returns the specified id document from the database
#Raises exception if the document doesnt exist
@app.get('/todo/{id}')
async def get_todo(id:int):
    try:
        return docEntity(col.find_one(id))

    except:
        raise HTTPException(status_code=404,detail="Todo Not Found")


#Updates a todo with specified id with required values
#must include all the attributes of class Todo in the update parameters
#Raises exception if the document doesnt exist
@app.put('/todo/{id}')
async def update_todo(id:int, todo: Todo):
    try:
        obj = col.find_one_and_update({"_id": id},{"$set":todo},upsert=True)
        return docEntity(obj)

    except:
        raise HTTPException(status_code=404,detail="Todo Not Found")


#deletes a specified document from the database using id of the document
#raises exception if the document doesnt exist
@app.delete('/todo/{id}')
async def delete_item(id: int):
    try:
        obj = col.find_one(id)
        col.find_one_and_delete({"_id": id})
        return docEntity(obj)
    except:
        raise HTTPException(status_code=404,detail="Todo Not Found")

