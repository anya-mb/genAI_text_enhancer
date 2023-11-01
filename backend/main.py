from fastapi import FastAPI
from pydantic import BaseModel


class TextModel(BaseModel):
    text: str


app = FastAPI()


@app.post("/reverse/")
async def reverse_text(item: TextModel):
    return {"reversed": item.text[::-1]}
