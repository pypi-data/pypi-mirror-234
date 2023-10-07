import os
from typing import Dict, Tuple, List, TypeVar
from typing_extensions import Literal

from pydantic import validate_model, BaseModel

T = TypeVar('T', bound=BaseModel)


class MissingUserData(BaseModel):
    env_prefix: str
    fields: List[str] = []
    err_kind: Literal['missing_user_data'] = 'missing_user_data'


class RequiredToken(MissingUserData):
    service: str
    err_kind: Literal['required_token'] = 'required_token'


def complete_settings(obj: T, prefix: str, user_data: Dict[str, str]) -> Tuple[T, List[str]]:
    new_info = {}
    for f in obj.__fields__:
        if f in obj.__fields_set__:
            continue
        currentVal = getattr(obj, f)
        if currentVal is not None:
            continue
        new_value = user_data.get(prefix + f, None) or os.getenv(prefix + f)
        if new_value is not None:
            new_info[f] = new_value

    partial_model, keys, _ = validate_model(type(obj), new_info)
    partial_model = {k: partial_model[k] for k in keys}

    result = obj.copy(update=partial_model)
    missing_fields = []
    for f in result.__fields__:
        if f in result.__fields_set__:
            continue
        currentVal = getattr(obj, f)
        if getattr(obj, f) is None:
            missing_fields.append(f)

    return (result, missing_fields)
