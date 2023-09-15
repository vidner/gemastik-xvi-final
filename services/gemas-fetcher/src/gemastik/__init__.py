import os
from controllers import *
from typing import Optional, Any
from blacksheep import Application, Request, Response, JSONContent
from blacksheep.server.authorization import Policy
from guardpost.asynchronous.authentication import AuthenticationHandler, Identity
from guardpost.common import AuthenticatedRequirement
from guardpost.authorization import  UnauthorizedError
from blacksheep.server.responses import redirect
from blacksheep.server.templating import use_templates
from jinja2 import FileSystemLoader
from blacksheep_messages import *

app = Application()
    
app.serve_files("UI/assets")
app.use_sessions(os.urandom(32), session_cookie="gemastik_session")
use_templates(app, loader=FileSystemLoader("UI/views"))
use_blacksheep_message(app)

@app.router.get("/")
def index():
    return redirect('/auth/login')

redirect_url = "/"

class AuthHandler(AuthenticationHandler):
    def __init__(self):
        pass

    async def authenticate(self, context: Request) -> Optional[Identity]:
        global redirect_url
        session = context.session
        if session.get('login'):
            context.identity = Identity({"username" : session.get("username"), "id" : session.get("id")}, "GemasSession")
        else:
            redirect_url = "/auth/login"
            context.identity = None
        
        return context.identity


async def handle_unauthorized(app: Any, request: Request, http_exception: UnauthorizedError) -> Response:
    global redirect_url
    return redirect(redirect_url)

async def handle_404(app: Any, request: Request, http_exception: 404) -> Response:
    return Response(404, content=JSONContent({"status": 404, "message" : "404 not found"}))


app.use_authentication().add(AuthHandler())
app.use_authorization().add(Policy("authenticated", AuthenticatedRequirement()))
app.exceptions_handlers[UnauthorizedError] = handle_unauthorized
app.exceptions_handlers[404] = handle_404