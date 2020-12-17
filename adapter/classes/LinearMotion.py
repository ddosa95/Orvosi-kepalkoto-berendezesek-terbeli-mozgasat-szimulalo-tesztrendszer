import numpy as np

class LinearMotion:
    def __init__(self, direction_value, end_states_value):
        self.direction = direction_value
        if end_states_value:
            self.have_end_states = True
            self.downer_end_state = end_states_value[0]
            self.upper_end_state = end_states_value[1]
        else:
            self.have_end_states = False

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, direction_value):
        self.__direction = direction_value

    @property
    def downer_end_state(self):
        return self.__downer_end_state

    @downer_end_state.setter
    def downer_end_state(self, downer_end_state_value):
        self.__downer_end_state = downer_end_state_value

    @property
    def upper_end_state(self):
        return self.__upper_end_state

    @upper_end_state.setter
    def upper_end_state(self, upper_end_state_value):
        self.__upper_end_state = upper_end_state_value

    def is_reaching_end(self, position):
        if self.have_end_states:
            direction = np.array([0, 0, 0])
            i = 0
            for d in self.direction:
                x = 0 if d == 0 else 1/d
                direction[i] = x
                i += 1
            downer = np.dot(self.downer_end_state, self.direction)
            upper = np.dot(self.upper_end_state, self.direction)
            pos = np.dot(position, direction)
            if downer < pos < upper:
                return False
            else:
                return True

        return False


