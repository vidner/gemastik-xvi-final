import os
import json
from hashlib import sha256
from fastapi import FastAPI, Depends, Response, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from pasta import PastaSigner, PastaVerifier
import models


class Credential(BaseModel):
    username: str
    password: str
    role: str | None = 'user'


secret = b'\x00' + os.urandom(65)

app = FastAPI()


def auth(token):
    if token:
        splitted = token.split(" ")
        if len(splitted) == 2 and splitted[0] == "Bearer":
            return splitted[1]

    return False


@app.get('/')
def index(request: Request):
    token = auth(request.headers.get('Authorization'))
    if not token:
        return {"message": "Welcome to PASTA: Platform-Agnostic Security Token for Authentication"}

    verifier = PastaVerifier(secret)

    try:
        data = verifier.verify(token)
        if not data:
            return Response(json.dumps({"error": "Invalid token"}), 401)

        return data
    except Exception:
        return Response(json.dumps({"error": "Invalid token"}), 401)


@app.get('/flag')
def flag(request: Request):
    token = auth(request.headers.get('Authorization'))
    if not token:
        return Response(json.dumps({"error": "Invalid token"}), 401)

    verifier = PastaVerifier(secret)

    try:
        data = verifier.verify(token)
        if not data:
            return Response(json.dumps({"error": "Invalid token"}), 401)

        if data['role'] != 'admin':
            return Response(json.dumps({"error": "Only admin can see the flag"}), 403)

        flag = open('../flag.txt', 'r').read()
        return {"flag": flag}
    except Exception:
        return Response(json.dumps({"error": "Invalid token"}), 401)


@app.post("/auth")
def login(credential: Credential, version: int | None = 1, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(
        models.User.username == credential.username,
        models.User.password == sha256(credential.password.encode()).hexdigest()
    ).all()

    if len(users) != 1:
        return Response(json.dumps({"error": "Username/password is incorrect"}), 401)

    data = json.dumps({
        "username": users[0].username,
        "role": users[0].role
    })

    signer = PastaSigner(secret, version)
    token = signer.sign(data)

    return {"token": token}


@app.post("/register")
def register(credential: Credential, db: Session = Depends(get_db)):

    users = db.query(models.User).filter(
        models.User.username == credential.username
    ).all()

    if len(users) == 0:
        credential.password = sha256(credential.password.encode()).hexdigest()
        credential.role = "user"
        new_user = models.User(**credential.dict())

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return Response(json.dumps({"success": "User registered succesfully"}), 200)
    else:
        return Response(json.dumps({"error": "Username already exist"}), 409)
