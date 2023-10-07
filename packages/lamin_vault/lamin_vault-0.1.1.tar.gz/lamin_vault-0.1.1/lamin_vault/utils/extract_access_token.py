from typing import Union

from fastapi import Header


def extract_access_token(authentication: Union[str, None] = Header(default=None)):
    if authentication is not None:
        return authentication.split(" ")[1]
    return None
