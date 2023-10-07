# Copyright (c) 2022 Shapelets.io
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from blacksheep.server.openapi.common import EndpointDocs

__tags = ["Groups"]

group_name_doc = EndpointDocs(
    summary="Checks if a group name exists in the groups database",
    description="Returns a boolean flag indicating if a group name is already present in the system.",
    tags=__tags
)

__all__ = ['group_name_doc']
