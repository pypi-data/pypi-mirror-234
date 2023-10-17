from collections import Counter
from dataclasses import dataclass, field
from typing import Iterable, List, Optional

@dataclass(init=True, repr=True, order=False, frozen=True)
class Server:
    host: str
    port: int

@dataclass(init=True, repr=True, order=False, frozen=True)
class Service:
    name: str
    namespace: str
    call: str
    endpoint: Optional[str] = None
    timeout: Optional[int] = None


@dataclass(init=True, repr=True, order=False, frozen=True)
class Configuration:
    server: Server
    services: List[Service] = field(default_factory=list)
