from typing import Optional, Any
from blacksheep.server.controllers import Controller
from blacksheep.messages import Request, Response
from blacksheep.utils import join_fragments
from blacksheep.server.templating import view
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256

class TemplatingNotConfiguredException(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Server side HTML templating is not configured. Configure templating using "
            "the function `use_templates` from blacksheep.server.templating."
        )

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class BaseController(Controller):
    model: dict = {}
    session: dict = {}

    async def on_request(self, request: Request):
        if 'login' in request.session:
            if request.session['login']:
                def get_copy():
                    now = datetime.now()
                    return "{} {}".format(now.year, "Gemastik")

                self.model = {"session" : request.session, "copy" : get_copy}
                self.session = request.session

    @classmethod
    def route(cls):
        cls_name = cls.class_name()
        if cls_name.lower() != "index":
            return join_fragments(cls_name.lower())

    def view(
        self, name: Optional[str] = None, model: Optional[Any] = None, **kwargs
    ) -> Response:

        final_model = {}

        if name is None:
            name = self.get_default_view_name()

        if self.templates is None:
            raise TemplatingNotConfiguredException()
        
        if self.model:
            final_model = { **self.model } 

        if model:
            final_model = {**model, **final_model}

        return view(self.templates, self.full_view_name(name), final_model, **kwargs)
