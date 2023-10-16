from typing import Dict, List, Tuple
from .JsonParser import JsonParser
from .Controllers.MecanumMoveController import MecanumMoveController
from .Models.Motor import Motor
from .Controllers.JointController import JointController
from .Models.SerializableCommands import SerializableCommands
from .ServoConnection import ServoConnection



class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AdamManager(metaclass=MetaSingleton):
    def __init__(self) -> None:
        # Инициализация контроллера
        self.motors = self._parseConfigJson()  # Парсинг конфигурационного файла JSON
        self.name_to_motor = self._create_name_to_motor_mapping()  # Создание отображения имени мотора на объект мотора
        self.servo_connection = ServoConnection()  # Инициализация соединения с сервоприводом
        self._initialize_joint_controllers()  # Инициализация контроллеров сочленений
        self._initialize_joint_speed()
        self.move_controller = MecanumMoveController()  # Инициализация контроллера движения

        self._update()

    def _initialize_joint_speed(self):
        for motor in self.name_to_motor.values():
            joint = motor.joint_controller
            joint.set_speed(joint._joint.speed)
    
    def _parseConfigJson(self) -> List[Motor]:
        # Парсинг конфигурационного файла JSON и возвращение списка моторов
        motors = JsonParser.parse_config_json()
        #TODO: Тут пахнет грязно
        for motor in motors:
            motor.start_position = motor.target_position
        return motors

    def _create_name_to_motor_mapping(self) -> Dict[str, Motor]:
        # Создание отображения имени мотора на объект мотора
        return {motor.name: motor for motor in self.motors}

    def _initialize_joint_controllers(self):
        # Инициализация контроллеров сочленений для каждого мотора
        for motor in self.motors:
            motor.joint_controller.set_servo_connection(self.servo_connection)

    def _set_motor_target_position(self, motor_name: str, target_position: float, speed: float):
        # Установка целевой позиции и скорости для мотора
        motor = self.name_to_motor[motor_name]
        motor.target_position = target_position
        joint = motor.joint_controller
        if speed != 0 & joint._joint.speed != speed:
            joint.set_speed(speed)

    def _update(self):
        # Обновление позиций моторов и отправка команд сервоприводу
        for motor in self.name_to_motor.values():
            joint = motor.joint_controller
            joint.rotate_to(motor.target_position)
            motor.present_position = joint.get_present_position()

        self.servo_connection.execute_command_servo()

    def handle_command(self, commands: SerializableCommands):
        # Обработка команд и установка целевых позиций и скоростей для моторов
        for command in commands.motors:
            self._set_motor_target_position(
                command.name, command.goal_position, command.speed)
        self._update()

    def return_to_start_position(self):
        # Установка целевых позиций для всех моторов в исходные позиции и обновление
        for motor in self.motors:
            motor.target_position = motor.start_position
        self._update()

    def move(self, linear_velocity: Tuple[float, float], angular_velocity: float) -> None:
        # Управление движением моторов на основе линейных и угловых скоростей
        self.move_controller.move(linear_velocity, angular_velocity)
