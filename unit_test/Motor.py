from unit_test import connect
import unit_test_main as main



class Motor:
    def __init__(self, name_value, target_url_value, program_value=[]):
        self.name = name_value
        self.target_url = target_url_value
        self.program = program_value
        self.state = ''
        self.speed = 0
        self.ended = False

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name_value):
        self.__name = name_value

    @property
    def target_url(self):
        return self.__target_url

    @target_url.setter
    def target_url(self, target_url_value):
        self.__target_url = target_url_value

    @property
    def program(self):
        return self.__program

    @program.setter
    def program(self, program_value):
        self.__program = program_value

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state_value):
        self.__state = state_value
        self.turn_on_off_api_call()

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed_value):
        self.__speed = speed_value
        self.speed_api_call()

    def turn_on_off_api_call(self):
        if self.state != '' and self.target_url != '':
            state = f"/commands/{self.state}"
            connect.put_request(self.target_url, state)
        if self.state == 'On':
            connect.put_request(self.target_url, "/commands/Init")

    def speed_api_call(self):
        if self.target_url is not None and self.state == 'On':
            speed = str(self.speed)
            connect.put_request(self.target_url, "/commands/SetSpeed", speed)

    def tick(self, actual_time):
        delta_time = actual_time - main.START_TIME
        task_time = 0
        if self.program is not None and len(self.program) != 0:
            i = 0
            for task in self.program:
                if task_time <= delta_time < task_time + task['time'] and self.speed != task['speed']:
                    self.speed = task['speed']
                    break

                task_time += task['time']
                i +=1

            if i == len(self.program) and task_time < delta_time:
                self.speed = 0
                self.ended = True







