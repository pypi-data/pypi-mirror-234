from typing import Any


class Motor:
    name: str
    joint_controller: Any
    start_position:float
    target_position: float
    present_position: int

    def __init__(self, name: str, joint_controller: Any, target_position: float = 0) -> None:
        self.name = name
        self.joint_controller = joint_controller
        self.target_position = target_position
        self.present_position = 0
        self.start_position = 0