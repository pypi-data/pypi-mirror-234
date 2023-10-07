from .entity import uSwidEntity as uSwidEntity
from .enums import uSwidVersionScheme as uSwidVersionScheme
from .errors import NotSupportedError as NotSupportedError
from .evidence import uSwidEvidence as uSwidEvidence
from .link import uSwidLink as uSwidLink
from .payload import uSwidPayload as uSwidPayload
from _typeshed import Incomplete
from typing import List, Optional

class uSwidIdentity:
    tag_version: Incomplete
    software_version: Incomplete
    version_scheme: Incomplete
    summary: Incomplete
    product: Incomplete
    colloquial_version: Incomplete
    revision: Incomplete
    edition: Incomplete
    persistent_id: Incomplete
    lang: str
    generator: Incomplete
    payloads: Incomplete
    evidences: Incomplete
    def __init__(self, tag_id: Optional[str] = ..., tag_version: int = ..., software_name: Optional[str] = ..., software_version: Optional[str] = ..., generator: Optional[str] = ...) -> None: ...
    @property
    def software_name(self) -> Optional[str]: ...
    @property
    def generator_href(self) -> Optional[str]: ...
    @property
    def tag_id(self) -> Optional[str]: ...
    @software_name.setter
    def software_name(self, software_name: Optional[str]) -> None: ...
    def merge(self, identity_new: uSwidIdentity) -> None: ...
    def add_entity(self, entity: uSwidEntity) -> None: ...
    def add_link(self, link: uSwidLink) -> None: ...
    def add_payload(self, payload: uSwidPayload) -> None: ...
    def add_evidence(self, evidence: uSwidEvidence) -> None: ...
    @property
    def links(self) -> List[uSwidLink]: ...
    @property
    def entities(self) -> List[uSwidEntity]: ...
