import tempfile
from base64 import b64encode
from subprocess import check_output

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel


class Input(BaseModel):
    code: bytes


class Output(BaseModel):
    output: bytes


app = FastAPI()


@app.get("/")
def index():
    return FileResponse("index.html")


@app.post("/api/run")
def run(input: Input):
    code = input.code

    with tempfile.NamedTemporaryFile() as fp:
        fp.write(code)
        fp.seek(0)
        output = check_output(["./hirnfick", fp.name])

    return Output(output=b64encode(output))
