from pydantic import BaseModel
from typing import List, Optional


class FunctionProfile(BaseModel):
    body: str
    parameters: Optional[List]
    result: Optional[str] = None
