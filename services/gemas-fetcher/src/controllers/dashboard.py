import subprocess, zlib, gzip, json, urllib.request
from dataclasses import dataclass
from urllib.parse import urlparse
from .BaseController import BaseController
from blacksheep.server.controllers import get, post
from blacksheep.server.authorization import auth
from guardpost.asynchronous.authentication import Identity
from blacksheep import FromFiles, Response, Content
from datetime import datetime
from models import *

class Dashboard(BaseController):
    @auth()
    @get()
    async def index(self, user: Identity):
        return self.view()
    
    @auth()
    @get('/sample')
    async def sample_google(self):
        return Response(200, content=Content(b"text/plain", b'\x00\x00\x1f\x8b\x08\x00 $\x00e\x02\xff\x016\x00\xc9\xffx\x9c\xabV*(\xca/\xcbLI-R\xb2RP*OO-Q\xd2QP*-\xca\x01q3JJ\n\x8a\xad\xf4\xf5\xd3\xf3\xf3\xd3sR\xf5\x92\xf3s\x95j\x01\x93\x10\x103\x00bQS6\x00\x00\x00'))
    
    @auth()
    @post('/fetch_by_file')
    async def fetch_by_file(self, file: FromFiles):
        try:
            provider = {b"\x00\x00": "wget", b"\x00\x01" : "curl", b"\x00\x02": "python"}
            f = file.value[0]
            flags = f.data[:2]
            data = json.loads(zlib.decompress(gzip.decompress(f.data[2:])))

            if data["provider"] != provider[flags]:
                return str("Available provider : {wget, curl, python}")
            
            if urlparse(data["url"]).scheme in ["file", "ftp" ]:
                return str("You cannot use this scheme!!")
            
            if urlparse(data["url"]).hostname in ["localhost", "127.0.0.1"]:
                return str("Cannot fetch localhost / 127.0.0.1")
            
            if data["provider"] == "curl":
                return subprocess.check_output(["curl", data["url"]]).decode()
            
            if data["provider"] == "wget":
                return subprocess.check_output(["wget", data["url"], "-O", "-"]).decode()
            
            if data["provider"] == "python":
                return urllib.request.urlopen(data["url"]).read()
        except Exception as e:
            print(e)
            return str("Unknown Error")



