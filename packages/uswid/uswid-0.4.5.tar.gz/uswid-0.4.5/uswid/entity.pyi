from _typeshed import Incomplete
from enum import IntEnum
from typing import List, Optional

class uSwidEntityRole(IntEnum):
    TAG_CREATOR: int
    SOFTWARE_CREATOR: int
    AGGREGATOR: int
    DISTRIBUTOR: int
    LICENSOR: int
    MAINTAINER: int

class uSwidEntity:
    name: Incomplete
    regid: Incomplete
    roles: Incomplete
    def __init__(self, name: Optional[str] = ..., regid: Optional[str] = ..., roles: Optional[List[uSwidEntityRole]] = ...) -> None: ...
