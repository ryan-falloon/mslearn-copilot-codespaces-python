import os
import base64
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field


current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")


class Body(BaseModel):
    length: Union[int, None] = Field(20, ge=1, description="positive")


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.post('/generate')
def generate(body: Body):
    """
    Generate a pseudo-random token ID of twenty characters by default.
    Example POST request body:

    {
        "length": 20
    }
    """
    string = base64.b64encode(os.urandom(64))[:body.length].decode(
        'utf-8'
    )
    return {'token': string}


class TextInput(BaseModel):
    text: str

# Create a FastAPI endpoint that accepts a POST request with a JSON body
# containing a single field called "text" and returns a checksum of the text.


@app.post('/checksum')
def checksum(body: TextInput):
    """
    Generate a checksum of the text input. Example POST request body:

    {
        "text": "Hello, world!"
    }
    """
    checksum_value = sum(ord(char) for char in body.text)
    return {'checksum': checksum_value}
