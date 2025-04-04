from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Movement:
    x_axis: int = field(default=0)
    y_axis: int = field(default=0)
    z_axis: int = field(default=0)
    yaw: int = field(default=0)

    def __str__(self) -> str:
        return f"Movement(x={self.x_axis}, y={self.y_axis}, z={self.z_axis}, yaw={self.yaw})"

    def __repr__(self) -> str:
        return self.__str__()

    def set(self, x: Optional[int] = None, y: Optional[int] = None, z: Optional[int] = None, yaw: Optional[int] = None):
        if x is not None:
            if not isinstance(x, int):
                raise TypeError(f"x must be an int, got {type(x).__name__}")
            self.x_axis = x if x is not None else 0
        if y is not None:
            if not isinstance(y, int):
                raise TypeError(f"y must be an int, got {type(y).__name__}")
            self.y_axis = y if y is not None else 0
        if z is not None:
            if not isinstance(z, int):
                raise TypeError(f"z must be an int, got {type(z).__name__}")
            self.z_axis = z if z is not None else 0
        if yaw is not None:
            if not isinstance(yaw, int):
                raise TypeError(f"yaw must be an int, got {type(yaw).__name__}")
            self.yaw = yaw if yaw is not None else 0
