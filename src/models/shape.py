from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Shape:
    name: str = field(default=None)
    color: str = field(default=None)
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self):
        return f"{self.color} {self.name} detected at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    def __repr__(self):
        return self.__str__()
