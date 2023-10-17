import multiprocessing
import serial
import logging
import time
import math


class Tactigon_Serial(multiprocessing.Process):
    def __init__(
        self,
        com_port,
        data_a_pipe=False,
        data_b_pipe=False,
        angle_a_pipe=False,
        angle_b_pipe=False,
        debug=False,
    ):

        super(Tactigon_Serial, self).__init__(
            target=self.loop_iterator,
            args=(
                com_port,
                data_a_pipe,
                data_b_pipe,
                angle_a_pipe,
                angle_b_pipe,
                debug,
            ),
        )

    def loop_iterator(
        self, com_port, data_a_pipe, data_b_pipe, angle_a_pipe, angle_b_pipe, debug
    ):

        print("Tactigon Serial ", com_port, " object created")
        self.data_a_pipe = data_a_pipe
        self.data_b_pipe = data_b_pipe
        self.angle_a_pipe = angle_a_pipe
        self.angle_b_pipe = angle_b_pipe

        self.debug = debug
        self.timer = time.perf_counter()

        ser = serial.Serial()

        ser.baudrate = 115200
        ser.port = com_port

        ser.open()

        ser.reset_input_buffer()

        for _ in range(0, 500):
            ser.readline()

        print("Serial process started")

        while True:
            self.loop(ser)

    def loop(self, ser):
        """serial process loop"""

        string = str(ser.readline())
        string = string[2:-3]  # get rid of string init ' and end \n'

        string_list = list(string.split(" "))

        if len(string_list) == 10:

            string_list = list(string.split(" "))
            self.new_data = string_list[1:7]
            self.new_angle = string_list[7:10]

            # get lock and add new data
            if string_list[0] == "A":
                self.gravity_comp("A")

                if self.data_a_pipe != False:
                    self.data_a_pipe.send(self.new_data)

                if self.angle_a_pipe != False:
                    self.angle_a_pipe.send(self.new_angle)

            else:
                self.gravity_comp("B")
                if self.data_b_pipe != False:
                    self.data_b_pipe.send(self.new_data)

                if self.angle_b_pipe != False:
                    self.angle_b_pipe.send(self.new_angle)

        if self.debug:
            tstop = time.perf_counter()
            print(tstop - self.timer)
            self.timer = tstop

    def gravity_comp(self, tactigon):
        """gravity compensation"""

        G_CONST = 9.81
        ANG_TO_RAD = math.pi / 180
        ACC_RATIO = 1000
        VEL_RATIO = 30

        if tactigon == "A":
            self.new_data[0] = -float(self.new_data[0]) / ACC_RATIO # type: ignore
            self.new_data[1] = -float(self.new_data[1]) / ACC_RATIO # type: ignore
            self.new_data[2] = -float(self.new_data[2]) / ACC_RATIO # type: ignore

            self.new_data[3] = -float(self.new_data[3]) / VEL_RATIO # type: ignore
            self.new_data[4] = -float(self.new_data[4]) / VEL_RATIO # type: ignore
            self.new_data[5] = -float(self.new_data[5]) / VEL_RATIO # type: ignore

        else:
            self.new_data[0] = float(self.new_data[0]) / ACC_RATIO # type: ignore
            self.new_data[1] = float(self.new_data[1]) / ACC_RATIO # type: ignore
            self.new_data[2] = -float(self.new_data[2]) / ACC_RATIO # type: ignore

            self.new_data[3] = float(self.new_data[3]) / VEL_RATIO # type: ignore
            self.new_data[4] = float(self.new_data[4]) / VEL_RATIO # type: ignore
            self.new_data[5] = -float(self.new_data[5]) / VEL_RATIO # type: ignore

        if tactigon == "A":
            pitch = float(self.new_angle[0]) * ANG_TO_RAD
            roll = float(self.new_angle[1]) * ANG_TO_RAD
        else:
            pitch = -float(self.new_angle[0]) * ANG_TO_RAD
            roll = -float(self.new_angle[1]) * ANG_TO_RAD

        if self.new_data[2] == 0:
            beta = math.pi / 2
        else:
            beta = math.atan(
                math.sqrt(math.pow(self.new_data[0], 2) + math.pow(self.new_data[1], 2))
                / self.new_data[2]
            )

        self.new_data[0] = float(self.new_data[0]) - G_CONST * math.sin(roll) # type: ignore
        self.new_data[1] = float(self.new_data[1]) + G_CONST * math.sin(pitch) # type: ignore
        self.new_data[2] = float(self.new_data[2]) - G_CONST * math.cos(beta) # type: ignore


# Start point of the application
if __name__ == "__main__":
    from ..utilities.Config_Manager import Config_Manager

    # logging
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.DEBUG)

    # import json config
    hal_config = Config_Manager.from_file("hal.json")

    com_port = hal_config.get("SERIAL_COM_PORT")

    # create serial process
    pro = Tactigon_Serial(com_port, debug=True)

    input("type to strat serial process")
    pro.start()

    input("type any key to termninate ")
    pro.terminate()
