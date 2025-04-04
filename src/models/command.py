from dataclasses import dataclass, field
from typing import Optional

from .movement import Movement


@dataclass
class Command:
    type: str
    movement: Optional[Movement] = field(default=None)
    action: Optional[str] = field(default=None)

    def __str__(self) -> str:
        return f"{self.type.capitalize()} command"

    def __repr__(self) -> str:
        return self.__str__()

    def set(self, type: str, movement: Optional[Movement] = None, action: Optional[str] = None) -> None:
        """Sets the command properties."""
        if type not in ["movement", "action"]:
            raise ValueError("Invalid command type.")

        if type == "movement":
            if not isinstance(movement, Movement):
                raise ValueError("Movement command requires a valid Movement object.")
            self.movement = movement
            self.action = None

        if type == "action":
            if not isinstance(action, str):
                raise ValueError("Action command requires a valid action string.")
            self.action = action
            self.movement = None

        self.type = type
