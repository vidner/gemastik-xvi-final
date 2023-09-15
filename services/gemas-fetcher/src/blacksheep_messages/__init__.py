from typing import Optional
from blacksheep.server import Application
from blacksheep import URL
from blacksheep.client.cookies import CookieJar
from blacksheep.cookies import Cookie

from jinja2 import Environment

import json, os

class BlacksheepMessages:
    def __init__(self):
        self.cookies = CookieJar()
        self.site = URL(os.getenv('APP_URI').encode())
        self.domain = self.site.host.lower().decode()

        self.path = '/'

        uri_path = self.site.path
        if not uri_path or not uri_path.startswith(b"/") or uri_path.count(b"/") == 1:
            self.path = '/'
        else:
            self.path =  uri_path[0 : uri_path.rfind(b"/")].decode()
    
    def add(self, message: str, category: str = "default"):
        setCookie = Cookie(
                f"_bs_message_{category}",
                json.dumps([message]),
                http_only=True
        )

        checkIfExist = self.cookies.get(self.domain, self.path, setCookie.name.lower())

        if checkIfExist:
            self.cookies.remove(self.domain, self.path, setCookie.name.lower())
            setCookie.value = json.dumps( json.loads(checkIfExist.cookie.value) + [message] )
        
        self.cookies.add(
            URL(os.getenv('APP_URI').encode()),
            setCookie
        )
    
    def get(self, category: str, check=False):
        checkIfExist = self.cookies.get(self.domain, self.path, f"_bs_message_{category}".lower())
        if not checkIfExist:
            return []
        messages = checkIfExist.cookie.value
        if not check:
            self.cookies.remove(self.domain, self.path, f"_bs_message_{category}".lower())
        return json.loads(messages) or []
        
    

def __configure_services(
        app: Application
    ) -> None:

    blacksheep_message = BlacksheepMessages()
    app.services.add_instance(blacksheep_message)
    app.services.add_alias("bs_message", BlacksheepMessages)

    def bs_get_message(category:str = "default", check=False):
        services = app._service_provider
        cookie = services.get("bs_message")
        return cookie.get(category, check=check)
    
    helpers = {"_": lambda x: x, "bs_message" : bs_get_message }
    env: Environment = app.jinja_environment  # type: ignore
    env.globals.update(helpers)


def use_blacksheep_message(
        app: Application
    ) -> None:

    __configure_services(
        app
    )