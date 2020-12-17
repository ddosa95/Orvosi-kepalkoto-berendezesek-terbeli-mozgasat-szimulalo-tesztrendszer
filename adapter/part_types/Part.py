from adapter.collision_test import vector_transformations as calc, vector_transformations as vt
import numpy as np


class Part:

    def __init__(self,
                 name_value,
                 position_value,
                 extension_value,
                 rotation_value):
        self.name = name_value
        self.position = position_value
        self.extension = extension_value
        self.rotation = rotation_value
        self.exclude_test_with = []
        self.linear_motion = {}
        self.rotating_motion = {}

    @property
    def linear_motion(self):
        return self.__linear_motion_data

    @linear_motion.setter
    def linear_motion(self, linear_motion_data_value):
        self.__linear_motion_data = linear_motion_data_value

    @property
    def exclude_test_with(self):
        return self.__exclude_test_with

    @exclude_test_with.setter
    def exclude_test_with(self, exclude_test_with_value):
        self.__exclude_test_with = exclude_test_with_value

    @property
    def rotating_motion(self):
        return self.__rotating_motion

    @rotating_motion.setter
    def rotating_motion(self, rotating_motion_value):
        self.__rotating_motion = rotating_motion_value

    def get_axis_parallel_unit_vector(self):
        axis_vector = np.array([self.extension[0][0], 0, 0])
        axis_parallel_vector = calc.rotate(axis_vector, self.rotation)
        axis_parallel_unit_vector = axis_parallel_vector / np.linalg.norm(axis_parallel_vector)
        return axis_parallel_unit_vector

    def get_up_parallel_unit_vector(self):
        up_vector = np.array([0, self.extension[0][1], 0])
        up_parallel_vector = calc.rotate(up_vector, self.rotation)
        up_parallel_unit_vector = up_parallel_vector / np.linalg.norm(up_parallel_vector)
        return up_parallel_unit_vector

    def get_face_parallel_unit_vector(self):
        face_vector = np.array([0, 0, self.extension[0][2]])
        face = calc.rotate(face_vector, self.rotation)
        face_parallel_unit_vector = face / np.linalg.norm(face)
        return face_parallel_unit_vector

    def calculate_vertices(self):
        axis = self.extension[0][0] / 2
        up = self.extension[0][1] / 2
        face = self.extension[0][2] / 2
        rectangle_vertices = []
        for i in range(2):
            for j in range(2):
                for (k) in range(2):
                    rectangle_vertices.append([((-1) ** i) * axis, ((-1) ** j) * up, ((-1) ** k) * face])

        real_vertices = []
        for vertex in rectangle_vertices:
            real_vertices.append(calc.shift(calc.rotate(vertex, self.rotation), self.position))


        return real_vertices

    def get_collision_test_parameters(self):

        axis_parallel_unit_vector = self.get_axis_parallel_unit_vector()
        up_parallel_unit_vector = self.get_up_parallel_unit_vector()
        face_parallel_unit_vector = self.get_face_parallel_unit_vector()

        unit_vectors = {"axis_parallel": axis_parallel_unit_vector,
                        "up_parallel": up_parallel_unit_vector,
                        "face_parallel": face_parallel_unit_vector}

        half_axis = self.extension[0][0] / 2
        half_up = self.extension[0][1] / 2
        half_face = self.extension[0][2] / 2

        params = {"position": self.position,
                  "unit_vectors": unit_vectors,
                  "half_axis": half_axis,
                  "half_up": half_up,
                  "half_face": half_face
                  }

        return params

    def tick(self, world_handler):
        if self.rotating_motion:
            if self.rotating_motion.is_reaching_end(self.rotation):
                world_handler.simulation_is_running = False
                warning_message = " reach its rotating end state!!!"
                print(f"{self.name}{warning_message}")

        if self.linear_motion:
            if self.linear_motion.is_reaching_end(self.position):
                world_handler.simulation_is_running = False
                warning_message = " reach its linear end state!!!"
                print(f"{self.name}{warning_message}")

    def linear_moving(self, velocity):
        self.position = np.add(self.position, velocity * self.linear_motion.direction)
        if self.rotating_motion:
            self.rotating_motion.centre_point = np.add(self.rotating_motion.centre_point,
                                                       velocity * self.linear_motion.direction)

    def rotating_moving(self, rotation_velocity):
        self.rotation = np.add(self.rotation, rotation_velocity * self.rotating_motion.axis)
        self.position = np.add(self.rotating_motion.centre_point,
                               vt.rotate(self.position - self.rotating_motion.centre_point,
                                         rotation_velocity * self.rotating_motion.axis))
