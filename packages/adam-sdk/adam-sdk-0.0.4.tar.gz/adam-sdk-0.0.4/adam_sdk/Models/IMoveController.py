from abc import ABC, abstractmethod
from typing import Tuple
from .Motor import Motor

class IMoveController(ABC):
    @abstractmethod
    def move(self, linear_velocity: Tuple[float, float], angular_velocity: float) -> None:
        pass
