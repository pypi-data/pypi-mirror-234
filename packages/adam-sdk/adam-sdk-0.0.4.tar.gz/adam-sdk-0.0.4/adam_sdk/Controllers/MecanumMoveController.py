from typing import Tuple
from .MotorController import MotorController
from pymodbus.client.serial import ModbusSerialClient as ModbusClient

class MecanumMoveController:
    def __init__(self):
        client = ModbusClient(
            method="rtu", port="/dev/ttyS0", stopbits=1, bytesize=8, parity='N', baudrate=76800
        )
        client.connect()
        
        self.front_left = MotorController(client, 22, 2, 3)  # Создание объекта мотора для переднего левого колеса
        self.front_right = MotorController(client, 23, 0, 1, True)  # Создание объекта мотора для переднего правого колеса с инверсией
        self.rear_left = MotorController(client, 22, 0, 1)  # Создание объекта мотора для заднего левого колеса
        self.rear_right = MotorController(client, 23, 2, 3, True)  # Создание объекта мотора для заднего правого колеса с инверсией

    def move(self, linear_velocity: Tuple[float, float], angular_velocity: float) -> None:
        vx, vy = linear_velocity
        wz = angular_velocity
        
        speeds = [
            vy + vx + wz,
            vy - vx - wz,
            vy - vx + wz,
            vy + vx - wz
        ]
        
        max_speed = max(map(abs, speeds))  # Вычисление максимальной скорости среди всех колес

        if max_speed > 1:
            speeds = [speed / max_speed for speed in speeds]  # Нормализация скоростей, если максимальная скорость больше 1
        
        for motor, speed in zip([self.front_left, self.front_right, self.rear_left, self.rear_right], speeds):
            motor.set_speed(speed)
        
        # self.front_left.set_speed(speeds[0])  # Установка скорости для переднего левого колеса
        # self.front_right.set_speed(speeds[1])  # Установка скорости для переднего правого колеса
        # self.rear_left.set_speed(speeds[2])  # Установка скорости для заднего левого колеса
        # self.rear_right.set_speed(speeds[3])  # Установка скорости для заднего правого колеса
