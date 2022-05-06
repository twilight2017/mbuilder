from dataclasses import dataclass


@dataclass
class RepoInstance:
    floder: str
    hash: str
    image: str
    key: bool
    name: str = ""
