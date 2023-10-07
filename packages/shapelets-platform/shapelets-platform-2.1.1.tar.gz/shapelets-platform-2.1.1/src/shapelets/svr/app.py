import os

from blacksheep import Application, redirect, Request, text, json
from guardpost.asynchronous.authentication import AuthenticationHandler
from guardpost.authentication import Identity
from typing import Optional

from .docs import docs
from .model import SignedPrincipalId
from .settings import Settings


class ShapeletsAuthHandler(AuthenticationHandler):
    """
    Shapelets Auth Handler to identify the user using the application.
    """

    async def authenticate(self, context: Request) -> Optional[Identity]:
        header_value = context.get_first_header(b"Authentication")
        if header_value:
            token = header_value.decode('ascii').split("BEARER ", 1)[1]
            principal = SignedPrincipalId.from_token(token)
            if principal is None:
                raise RuntimeError(f'Invalid bearer token: {header_value}')

            identity = Identity({"userId": principal.userId})
            identity.access_token = token
            context.identity = identity
        else:
            context.identity = None
        return context.identity


async def ping():
    """
    Utility method to check if the HTTP API interface is running correctly.
    """
    return text("pong")


async def info():
    return text(os.getpid())


async def redirect_to_ui():
    return redirect("./app")


async def redirect_favicon():
    return redirect("./app/favicon.ico")


def setup_app(cfg: Settings) -> Application:
    # Create a root application
    app = Application(show_error_details=True)
    app.use_authentication().add(ShapeletsAuthHandler())

    # Necessary to handle correctly mounts, docs, etc..
    app.mount_registry.auto_events = True
    app.mount_registry.handle_docs = True

    # mount the UI as static under app
    app.serve_files(str(cfg.server.static),  # location
                    discovery=False,  # no listing
                    root_path='app',  # mounting point
                    allow_anonymous=True,  # app resources are freely accessible
                    fallback_document="index.html")  # support for html5 history api

    app.router.add_get("/", docs.ignore()(redirect_to_ui))
    app.router.add_get("/favicon.ico", docs.ignore()(redirect_favicon))
    app.router.add_get("/api/ping", docs.ignore()(ping))
    app.router.add_get("/api/info", docs.ignore()(info))

    # finally, bind the docs
    docs.bind_app(app)

    return app


# make app public
__all__ = ['setup_app']
