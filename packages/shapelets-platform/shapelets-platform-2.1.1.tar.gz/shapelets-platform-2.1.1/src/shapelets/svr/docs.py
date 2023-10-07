from blacksheep.server.openapi.v3 import OpenAPIHandler
from blacksheep.server.openapi.ui import ReDocUIProvider
from openapidocs.v3 import Info, Contact
from .._version import version

docs = OpenAPIHandler(
    info=Info(
        title="Shapelets API", 
        version=version, 
        description="TODO: Add description",
        contact=Contact("Shapelets", "https://shapelets.io", "info@shapelets.io")
    ),
    anonymous_access=True
)

docs.ui_providers.append(ReDocUIProvider())

__all__ = ['docs']
