import re

_ident_re = re.compile(r'^[A-Za-z_]\w*\Z')

def is_ident(v: str) -> bool:
    return bool(_ident_re.match(v))
