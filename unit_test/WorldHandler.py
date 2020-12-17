from unit_test import Motor
import json


class WorldHandler:
    def __init__(self):
        self.is_running = True
        self.motor_list = []

    def add_new_motor(self, motor_json):
        name = motor_json['name']
        path = motor_json.get("simulation_path")
        program = motor_json.get("program")
        new_motor = Motor.Motor(name, path, program)
        self.motor_list.append(new_motor)

    def load_motor(self, motor_program):
        with open(motor_program) as json_file:
            motor_list = json.load(json_file)
            for motor_json in motor_list['list']:
                self.add_new_motor(motor_json['motor'])

    def init(self):
        for motor in self.motor_list:
            motor.state = 'On'

    def tick(self, actual_time):
        i = 0
        for motor in self.motor_list:
            motor.tick(actual_time)
            if motor.ended:
                i += 1

        if i == len(self.motor_list):
            for motor in self.motor_list:
                motor.state = 'Off'
                self.is_running = False
