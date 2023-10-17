from pathlib import Path
from subprocess import Popen, PIPE
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

app = FastAPI()


class CMD(BaseModel):
    cmd: str


class PYCMD(BaseModel):
    exec_path: str
    py_scripts: str


origins = [
    "http://localhost:8080",
    "https://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/sh")
def exec_sh(cmd: CMD) -> bytes:
    popen = Popen(cmd.cmd, stdout=PIPE, stderr=PIPE, shell=True)
    popen.wait()
    error = popen.stderr.read()
    stdout = popen.stdout.read()
    if error:
        raise HTTPException(status_code=500, detail=error)
    return stdout


@app.post("/py")
def exec_py(py_cmd: PYCMD) -> bytes:
    fid = uuid.uuid4()
    fpath = Path(f"/tmp/{fid}")
    fpath.write_text(py_cmd.py_scripts)
    exec_path = Path(py_cmd.exec_path).absolute()
    popen = Popen(f"python {fpath}", stdout=PIPE, stderr=PIPE, shell=True, cwd=exec_path)
    popen.wait()
    error = popen.stderr.read()
    stdout = popen.stdout.read()
    if error:
        raise HTTPException(status_code=500, detail=error)
    return stdout


if __name__ == '__main__':
    uvicorn.run("remote_sh:app", port=8892, host="0.0.0.0")