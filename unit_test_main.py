from unit_test import WorldHandler
import time
from adapter import main as adapter_main

BASE_URL = "http://192.168.1.72:9000/tango/rest/rc4/hosts/tangobox-vm/10000/devices"
START_TIME = time.time()


def main():
    program = WorldHandler.WorldHandler()
    program.load_motor("../motor_program.json")
    program.init()

  #  adapter_main.main()
    while program.is_running:
        program.tick(time.time())


if __name__ == '__main__':
    main()
