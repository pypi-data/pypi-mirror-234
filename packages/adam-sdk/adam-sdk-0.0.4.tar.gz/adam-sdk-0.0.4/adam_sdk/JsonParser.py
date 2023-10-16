import os
import json
from .Controllers.JointController import JointController
from .Models.Joint import Joint
from .Models.Motor import Motor

current = os.path.dirname(os.path.realpath(__file__))

class JsonParser:

    @staticmethod
    def _read_config():
        config_file_path = "/etc/adam_configs/servo_range.config"
        
        if os.path.isfile(config_file_path) is False:
            config_file_path = f'{current}/../examples/servo_range.config'
        file = open(config_file_path)
        data = json.load(file)
        file.close()

        return data

    @staticmethod
    def read_command():
        #TODO должно быть удалено
        f = open(f'{current}/examples/SerializableCommandHead.json')
        data = json.load(f)
        f.close()

        return data

    @staticmethod
    def parse_config_json():
        config = JsonParser._read_config()
        motors = []
        for element in config:
            if 'target_position' in element:
                target_position = element['target_position']
            else:
                target_position = 0
            motors.append(Motor(name=element['name'],
                                target_position=target_position,
                                joint_controller=JointController(joint=Joint(element['joint']['lover_limit'],
                                                                            element['joint']['upper_limit'],
                                                                            element['joint']['speed'],
                                                                            element['joint']['id']))))
        return motors
