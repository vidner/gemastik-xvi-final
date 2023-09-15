from .BaseController import BaseController
from blacksheep.server.controllers import get, post
from blacksheep.messages import Request
from blacksheep.server.bindings import FromForm
from blacksheep.server.responses import redirect
from guardpost.asynchronous.authentication import Identity
from passlib.hash import pbkdf2_sha256 as sha256
from models import Users
from dataclasses import dataclass

@dataclass
class LoginForm:
    username: str
    password: str

@dataclass
class RegisterUser:
    username: str
    password: str

class Auth(BaseController):    
    @get('/')
    async def index(self):
        return redirect('/auth/login')
    
    @get('/login')
    async def login_page(self, user: Identity):
        if user:
            return redirect("/dashboard")

        return self.view()

    @post('/login')
    async def login_action(self, request: Request, data: FromForm[LoginForm], bs_message):
        getUser = Users.objects.filter(username=data.value.username).first()

        if not getUser:
            bs_message.add("Wrong Username or Password", "error")
            return redirect('/auth/login')

        if sha256.verify(data.value.password, getUser.password):
            request.session.update({
                "id" : str(getUser.id),
                "username" : getUser.username,
                "login" : True,
            })
            return redirect("/dashboard")
        
        bs_message.add("Wrong Username or Password", "error")
        return redirect("/auth/login")
    
    @get('/register')
    async def register_page(self, user: Identity):
        if user:
            return redirect("/dashboard")

        return self.view()
        

    @post('/register')
    async def register_action(self, data: FromForm[RegisterUser], bs_message):
        getUser = Users.objects.filter(username=data.value.username).first()

        if getUser:
            bs_message.add("Username already used, please use other username", "error")
            return redirect("/auth/register")

        user = Users(username=data.value.username, password=sha256.encrypt(data.value.password))
        user.save()

        bs_message.add("Success register", "success")
        return redirect("/auth/login")