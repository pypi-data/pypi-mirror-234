from .container import uSwidContainer as uSwidContainer
from .entity import uSwidEntityRole as uSwidEntityRole
from .format import uSwidFormatBase as uSwidFormatBase
from .hash import uSwidHashAlg as uSwidHashAlg
from .identity import uSwidIdentity as uSwidIdentity

class uSwidFormatCycloneDX(uSwidFormatBase):
    def __init__(self) -> None: ...
    def save(self, container: uSwidContainer) -> bytes: ...
