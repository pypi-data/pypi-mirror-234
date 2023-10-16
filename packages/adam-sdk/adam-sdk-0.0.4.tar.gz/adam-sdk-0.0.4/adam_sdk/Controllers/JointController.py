from ..Models.Joint import Joint
from ..ServoConnection import ServoConnection


class JointController:
    def __init__(self, joint: Joint) -> None:
        self._joint = joint  # Инициализация объекта Joint
        self._target_position = -1  # Инициализация целевой позиции
        self._servo_connection = None  # Инициализация объекта ServoConnection

    def rotate_to(self, target_position: float) -> None:
        if target_position != self._target_position:
            self._target_position = target_position  # Установка новой целевой позиции
            goal_position = ((self._joint.upper_limit - self._joint.lower_limit) *
                             (self._target_position / 100)) + self._joint.lower_limit  # Расчет целевой позиции сервопривода
            
            self._servo_connection.append_command_position_buffer((self._joint.id, goal_position))  # Добавление команды в буфер команд

    def set_speed(self, speed: int):
        self._servo_connection.append_command_speed_buffer((self._joint.id, self._joint.speed))
        self._joint.speed = speed  # Установка скорости сервопривода

    def set_servo_connection(self, servo_connection: ServoConnection):
        self._servo_connection = servo_connection  # Установка объекта ServoConnection

    def get_present_position(self):
        return self._target_position  # Получение текущей позиции сервопривода
