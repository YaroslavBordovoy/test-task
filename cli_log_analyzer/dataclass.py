from dataclasses import dataclass


@dataclass()
class NginxLog:
    ip: str
    timestamp: str
    method: str
    path_: str
    status: int
    response_size: int
