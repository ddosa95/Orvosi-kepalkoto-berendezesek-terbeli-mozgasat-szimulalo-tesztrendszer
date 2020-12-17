import numpy as np

class RotatingMotion:

    def __init__(self, centre_point_value, axis_value, end_states_value):
        self.centre_point = centre_point_value
        self.axis = axis_value
        if end_states_value:
            self.have_end_states = True
            self.downer_end_state = end_states_value[0]
            self.upper_end_state = end_states_value[1]
        else:
            self.have_end_states = False

    @property
    def centre_point(self):
        return self.__centre_point

    @centre_point.setter
    def centre_point(self, centre_point_value):
        self.__centre_point = centre_point_value

    @property
    def axis(self):
        return self.__axis

    @axis.setter
    def axis(self, axis_value):
        self.__axis = axis_value

    # @property
    # def downer_end_state(self):
    #     return self.__downer_end_state
    #
    # @downer_end_state.setter
    # def downer_end_state(self, downer_end_state_value):
    #     self.__downer_end_state = downer_end_state_value
    #
    # @property
    # def upper_end_state(self):
    #     return self.__upper_end_state
    #
    # @upper_end_state.setter
    # def upper_end_state(self, upper_end_state_value):
    #     self.__upper_end_state = upper_end_state_value

    def is_reaching_end(self, rotation):
        if self.have_end_states:
            axis = np.array([0, 0, 0])
            i = 0
            for a in self.axis:
                x = 0 if a == 0 else 1/a
                axis[i] = x
                i += 1
            downer = np.dot(self.downer_end_state, self.axis)
            upper = np.dot(self.upper_end_state, self.axis)
            rot = np.dot(rotation, self.axis)
            if downer < rot < upper:
                return False
            else:
                return True

        return False
