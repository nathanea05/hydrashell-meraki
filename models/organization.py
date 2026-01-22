# Library Imports
from dataclasses import dataclass
from typing import Optional

# Local Imports


@dataclass
class Organization:
    id: str
    name: str
    url: Optional[str] = None
    api: Optional[dict] = None
    licensing: Optional[dict] = None
    cloud: Optional[dict] = None
    management: Optional[dict] = None


    @classmethod
    def from_dict(cls, d: dict) -> Organization:
        return cls(
            id=str(d["id"]),
            name=d.get("name", ""),
            url=d.get("url", ""),
            api=d.get("api", ""),
            licensing=d.get("licensing", ""),
            cloud=d.get("cloud", ""),
            management=d.get("management", "")
        )