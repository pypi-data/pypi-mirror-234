# Copyright (c) 2022 Shapelets.io
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from blacksheep.server.openapi.common import (
    ContentInfo,
    EndpointDocs,
    HeaderInfo,
    RequestBodyInfo,
    ResponseExample,
    ResponseInfo,
)

__tags = ["Users"]

me_doc = EndpointDocs(
    summary="Current user profile",
    description="""Returns details of the current logged user""",
    tags=__tags
)

nickname_doc = EndpointDocs(
    summary="Checks if a user name exists in the user database",
    description="Returns a boolean flag indicating if a user name is already present in the system.",
    tags=__tags
)

__all__ = ['me_doc', 'nickname_doc']
