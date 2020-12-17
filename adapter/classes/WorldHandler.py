import json
from adapter.classes import LinearMotion, RotatingMotion
from adapter.collision_test import collision_test
from adapter.part_types import Part, Motor
import numpy as np


class WorldHandler:
    def __init__(self):
        self.dict_of_parts = {}
        self.simulation_is_running = True

    def add_new_part(self, new_json_part):
        name = new_json_part['part']['name']
        extension = np.array([new_json_part['part']['extension']])
        position = np.array(new_json_part['part']['position'])
        rotation = np.array(new_json_part['part']['rotation'])
        motor = new_json_part['part'].get('motor')
        rotating_motion = new_json_part['part'].get('rotating_motion')
        linear_motion = new_json_part['part'].get('linear_motion')

        if motor:
            target_names = motor.get('target_names')
            simulation_path = motor.get("simulation_path")
            new_part = Motor.Motor(name, position, extension, rotation, target_names, simulation_path)
        else:
            new_part = Part.Part(name, position, extension, rotation)

        if rotating_motion:
            centre_point = np.array(rotating_motion['rotation_centre_point'])
            axis = np.array(rotating_motion['rotation_axis'])
            end_states = rotating_motion.get('rotating_end_states')

            rot = RotatingMotion.RotatingMotion(centre_point, axis, end_states)
            new_part.rotating_motion = rot

        if linear_motion:
            direction = np.array(linear_motion['direction'])
            end_states = linear_motion.get('linear_end_states')

            lin = LinearMotion.LinearMotion(direction, end_states)
            new_part.linear_motion = lin

        self.dict_of_parts[name] = new_part

    def load_part_list(self, part_list_json):
        with open(part_list_json) as json_file:
            part_list = json.load(json_file)
            if part_list['json_type'] == 'part_list':
                for part_json in part_list['list']:
                    self.add_new_part(part_json)
                for exclude_pair in part_list['exclude_from_collision']:
                    self.dict_of_parts[exclude_pair[0]].exclude_test_with.append(exclude_pair[1])
                    self.dict_of_parts[exclude_pair[1]].exclude_test_with.append(exclude_pair[0])

            elif part_list['json_type'] == 'path_list':
                for part in part_list['list']:
                    new_part_location = part['path']
                    with open(new_part_location) as json_part_file:
                        new_json = json.load(json_part_file)
                    self.add_new_part(new_json)
                for exclude_pair in part_list['exclude_from_collision']:
                    self.dict_of_parts[exclude_pair[0]].exclude_test_with.append(exclude_pair[1])
                    self.dict_of_parts[exclude_pair[1]].exclude_test_with.append(exclude_pair[0])
            else:
                print("Invalid JSON file")

    def collision_test(self):
        p = 0

        for name_a, part_a in sorted(self.dict_of_parts.items()):
            for_test = {k: self.dict_of_parts[k] for k in self.dict_of_parts.keys() - set(part_a.exclude_test_with)}
            for name_b, part_b in sorted(for_test.items(), reverse=True):
                if name_a == name_b:
                    break

                if collision_test.are_collision(part_a, part_b):
                    self.simulation_is_running = False
                    warning_message = "The name = {}, and the name = {} parts will collides each other!!!"
                    print(warning_message.format(name_a,
                                                 name_b))
                else:
                    p += 1

    def tick(self):
        for part in self.dict_of_parts.values():
            part.tick(self)
        self.collision_test()
