from _typeshed import Incomplete
from enum import IntEnum
from typing import Optional

class uSwidHashAlg(IntEnum):
    UNKNOWN: int
    SHA256: int
    SHA384: int
    SHA512: int
    @classmethod
    def from_string(cls, alg_id: str) -> uSwidHashAlg: ...

class uSwidHash:
    alg_id: Incomplete
    def __init__(self, alg_id: Optional[uSwidHashAlg] = ..., value: Optional[str] = ...) -> None: ...
    @property
    def alg_id_for_display(self) -> Optional[str]: ...
    @property
    def value(self) -> Optional[str]: ...
