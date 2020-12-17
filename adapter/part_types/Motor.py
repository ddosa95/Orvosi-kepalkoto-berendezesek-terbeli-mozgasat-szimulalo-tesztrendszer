from adapter.part_types import Part
import json
from adapter import connect


class Motor(Part.Part):
    def __init__(self, name_value,
                 position_value,
                 extension_value,
                 rotation_value,
                 target_names_value,
                 simulation_path_value):
        super().__init__(name_value, position_value, extension_value, rotation_value)
        self.velocity = ""
        self.target_names = target_names_value
        self.simulation_path = simulation_path_value

    @property
    def velocity(self):
        return self.__velocity

    @property
    def target_names(self):
        return self.__target_names

    @property
    def simulation_path(self):
        return self.__simulation_path

    @simulation_path.setter
    def simulation_path(self, simulation_path_value):
        self.__simulation_path = simulation_path_value

    @target_names.setter
    def target_names(self, target_names_value):
        self.__target_names = target_names_value

    @velocity.setter
    def velocity(self, velocity_value):
        self.__velocity = velocity_value

    def get_speed(self):
        r = connect.request(self.simulation_path + "/attributes/speed/value")
        speed_json = json.loads(r)
        self.velocity = speed_json['value']

    def tick(self, world_handler):
        super(Motor, self).tick(world_handler)
        self.get_speed()

        for target_name in self.target_names:
            if self.target_names[target_name] == "linearly":
                world_handler.dict_of_parts[target_name].linear_moving(self.velocity)

            if self.target_names[target_name] == "rotationally":
                world_handler.dict_of_parts[target_name]

                world_handler.dict_of_parts[target_name].rotating_moving(self.velocity)
