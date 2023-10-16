from .container import uSwidContainer as uSwidContainer
from .entity import uSwidEntity as uSwidEntity, uSwidEntityRole as uSwidEntityRole
from .enums import uSwidGlobalMap as uSwidGlobalMap
from .errors import NotSupportedError as NotSupportedError
from .evidence import uSwidEvidence as uSwidEvidence
from .format import uSwidFormatBase as uSwidFormatBase
from .hash import uSwidHash as uSwidHash, uSwidHashAlg as uSwidHashAlg
from .identity import uSwidIdentity as uSwidIdentity
from .link import uSwidLink as uSwidLink, uSwidLinkRel as uSwidLinkRel
from .payload import uSwidPayload as uSwidPayload
from typing import Optional

class uSwidFormatCoswid(uSwidFormatBase):
    def __init__(self) -> None: ...
    def load(self, blob: bytes, path: Optional[str] = ...) -> uSwidContainer: ...
    def save(self, container: uSwidContainer) -> bytes: ...
