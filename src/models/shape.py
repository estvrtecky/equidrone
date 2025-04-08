from dataclasses import dataclass, field
from datetime import datetime
import math


@dataclass
class Shape:
    name: str = field(default=None)
    color: str = field(default=None)
    timestamp: datetime = field(default_factory=datetime.now)

    def __str__(self):
        return f"{self.color} {self.name} detected at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, value):
        if not isinstance(value, Shape):
            return False
        return self.name == value.name and self.color == value.color

    @property
    def age(self) -> int:
        """Returns the age of the shape in seconds."""
        return math.floor((datetime.now() - self.timestamp).total_seconds())
