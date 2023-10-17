__version__ = "3.0.3"

import multiprocessing
import logging
import sys
import time
from enum import Enum
from os import path

from typing import Optional
from multiprocessing.connection import PipeConnection

# resource directory - need to be referenced to exe path when used with exe bundle
# if getattr(sys, "frozen", False):
#     CLIENT_PY_PATH = sys._MEIPASS # type: ignore
# else:
#     CLIENT_PY_PATH = path.join(path.dirname(path.abspath(__file__)), "../")
#     sys.path.insert(0, path.join(CLIENT_PY_PATH, "utilities"))
#     sys.path.insert(0, path.join(CLIENT_PY_PATH, "hal"))
#     sys.path.insert(0, path.join(CLIENT_PY_PATH, "middleware"))

# from Config_Manager import Config_Manager
# from Tactigon_BLE import BLE
# from Tactigon_Gesture import Tactigon_Gesture
# from Tactigon_Speech import Tactigon_Speech, Phrase, HotWord
# from Tactigon_Speech_New import Tactigon_Speech as Tactigon_Speech_New, TDeepSpeech, TSpeechCommand, TSpeechObject, HotWord, TSpeech
# from License_Manager import License_Manager

# from .utilities.Config_Manager import Config_Manager, config_files_checks
# from .utilities.License_Manager import License_Manager
from .hal.Tactigon_BLE import BLE
from .middleware.Tactigon_Gesture import Tactigon_Gesture
from .middleware.Tactigon_Speech import Tactigon_Speech
from .middleware.Tactigon_Speech_New import Tactigon_Speech as Tactigon_Speech_New

from .models import HAL, RealTimeConfig, Voice, TGear_Pipes_Name, TGear_Connection_Status, Pipes, TSpeech_Version, AudioSource

class TGear_Engine:
    @property
    def version(self) -> str:
        return __version__

    hal: HAL
    real_time: RealTimeConfig
    voice: Voice

    debug: bool


    def __init__(self, hal: HAL, real_time: RealTimeConfig, voice: Voice, debug=False):
        '''
        Initialization routine for TGear_Engine class.
        It need to be called before configuration and sets the configuration objects.

        Args:
            hal (HAL)                                               : Hardware Abstraction Layer configuration
            real_time (RealTimeConfig)                              : Configuration for gesture model
            voice (Voice)                                           : Configuration for speech recognition
        Returns:
            none
        '''

        self.hal = hal
        self.real_time = real_time
        self.voice = voice
        self.debug = debug

        if self.debug:
            print("TGear Engine created")

        # init all (right and left) pipes to false
        self.pipes = {"RIGHT": Pipes(), "LEFT": Pipes()}
        self.enables = {"RIGHT": False, "LEFT": False}
        self.addr = {"RIGHT": "", "LEFT": ""}
        self.ble_process = {"RIGHT": None, "LEFT": None}
        self.gest_processes = {"RIGHT": False, "LEFT": False}
        self.voice_processes = {"RIGHT": None, "LEFT": None}

        # check license
        # if not License_Manager(debug).check_license() and False:
        #     print("Invalid license: TGear_Engine not available")
        #     return
        # else:
        #     print("License ok")

        # check config files
        # if not config_files_checks():
        #     return
        # else:
        #     print("Config files ok")

        if debug:
            # logging
            multiprocessing.log_to_stderr()
            logger = multiprocessing.get_logger()
            logger.setLevel(logging.DEBUG)

        # import json config
        # hal_config = Config_Manager.from_file("hal.json")
        self.addr["RIGHT"] = self.hal.BLE_RIGHT_ADDRESS
        self.addr["LEFT"] = self.hal.BLE_LEFT_ADDRESS
        self.enables["RIGHT"] = self.hal.BLE_RIGHT_ENABLE
        self.enables["LEFT"] = self.hal.BLE_LEFT_ENABLE
        self.num_sample = self.hal.NUM_SAMPLE

        # print info
        en_string = ["disabled", "enabled"]
        print(
            "RIGHT device ({}) is {}".format(
                self.addr["RIGHT"], en_string[self.enables["RIGHT"] == True]
            )
        )
        print(
            "LEFT device ({}) is {}".format(
                self.addr["LEFT"], en_string[self.enables["LEFT"] == True]
            )
        )

    def config(
        self,
        tacti="",
        gesture_pipe_en=False,
        acc_pipe_en=False,
        angle_pipe_en=False,
        button_pipe_en=False,
        voice_pipe_en=False,
        gesture_prob_th=0.85,
        confidence_th=5,
    ):
        '''
        Config TSkin device to be used on RIGHT or LEFT hand

        Use this function to activate/deactivate data exchange pipes

        Once a pipe is enabled and engine started, engine pushes data in tx side of pipe
        On the rx side of the pipe, user application can pull data from it using standard poll()/recv() multiprocessing module functions
        To avoid blocking of pipes, user application must in any case pull all data pushed in pipe by engine

        Args:
            tacti (str)                                             : "RIGHT" or "LEFT"
            gesture_pipe_en (bool)                                  : enable/disable(default) gesture pipe, where gestures are pushed by detection engine
            acc_pipe_en (bool)                                      : enable/disable(default) acceleration data pipe, where xyz accelerations coming from Tskin are pushed as continuous stream
            angle_pipe_en (bool)                                    : enable/disable(default) Eulero angles data pipe, where Roll, Pitch, Yaw angles coming from Tskin are pushed as continuous stream
            button_pipe_en (bool)                                   : enable/disable(default) buttons data pipe, where buttons status coming from Tskin are pushed as continuous stream
            voice_pipe_en (bool)                                    : enable/disable(default) voice data pipe, where candidates are pushed by voice ai engine
            gesture_prob_th (float, range: 0 - 1, default=0.85)     : probability threshold. The detection of a gesture is condidered valid only if its probability is greater than this threshold 
            confidence_th (float, range: 0 - INF, defualt=5)        : confidence threshold. Confidence is the ration between first and second gestures in probability scoring. The detection of a gesture is condidered valid only if its confidence is greater than this threshold

        Returns:
            none
        '''
        

        gen_enable = self.enables[tacti]
        addr = self.addr[tacti]

        if gen_enable == True:

            # gesture pipe - if requested
            if gesture_pipe_en:
                (
                    self.pipes[tacti].sensor_rx,
                    self.pipes[tacti].sensor_tx,
                ) = multiprocessing.Pipe(duplex=False)
                (
                    self.pipes[tacti].gesture_rx, # type: ignore
                    self.pipes[tacti].gesture_tx, # type: ignore
                ) = multiprocessing.Pipe(duplex=False)

            # angle pipe - if requested
            if angle_pipe_en:
                (
                    self.pipes[tacti].angle_rx, # type: ignore
                    self.pipes[tacti].angle_tx, # type: ignore
                ) = multiprocessing.Pipe(duplex=False)

            # acc pipe - if requested
            if acc_pipe_en:
                (
                    self.pipes[tacti].acc_rx, # type: ignore
                    self.pipes[tacti].acc_tx, # type: ignore
                ) = multiprocessing.Pipe(duplex=False)

            # button pipe - if requested
            if button_pipe_en:
                (
                    self.pipes[tacti].button_rx, # type: ignore
                    self.pipes[tacti].button_tx, # type: ignore
                ) = multiprocessing.Pipe(duplex=False)

            # TODO: add voice on both tskins?

            if voice_pipe_en:
                (
                    self.pipes[tacti].voice_rx, # type: ignore
                    self.pipes[tacti].voice_tx, # type: ignore
                ) = multiprocessing.Pipe()
                if self.voice.tactigon_speech_version == TSpeech_Version.NEW and self.voice.audio_source == AudioSource.TSKIN:
                    (
                        self.pipes[tacti].adpcm_rx,
                        self.pipes[tacti].adpcm_tx,
                    ) = multiprocessing.Pipe(duplex=False)

            # create  BLE process
            self.ble_process[tacti] = BLE(  # type: ignore
                name=tacti,
                ble_address=addr,
                sensor_pipe=self.pipes[tacti].sensor_tx,
                angle_pipe=self.pipes[tacti].angle_tx, # type: ignore
                acc_pipe=self.pipes[tacti].acc_tx, # type: ignore
                button_pipe=self.pipes[tacti].button_tx, # type: ignore
                adpcm_pipe=self.pipes[tacti].adpcm_tx
                )
            
            # create gesture process - if requested
            if gesture_pipe_en:
                self.gest_processes[tacti] = Tactigon_Gesture( # type: ignore
                    self.real_time,
                    tacti,
                    self.num_sample,
                    self.pipes[tacti].sensor_rx,
                    self.pipes[tacti].gesture_tx,
                    gesture_prob_th=gesture_prob_th,
                    confidence_th=confidence_th,
                    debug=self.debug,
                )

            if voice_pipe_en:
                if self.voice.tactigon_speech_version == TSpeech_Version.OLD:
                    self.voice_processes[tacti] = Tactigon_Speech( # type: ignore
                        self.voice,
                        self.pipes[tacti].voice_tx # type: ignore
                    )
                else:
                    self.voice_processes[tacti] = Tactigon_Speech_New( # type: ignore
                        self.voice,
                        self.pipes[tacti].voice_tx, # type: ignore
                        self.pipes[tacti].adpcm_rx,
                        self.voice.audio_source
                    )

    def get_pipe(self, tacti, pipe_name):
        '''
        Get pipe to retrieve needed data
        In the following a summary of data format in each pipe:

        gesture pipe:   list[gesture_label(string), displacement(float), gesture probability(float), Confidence(long)]
        angles pipe:    list[roll(string), pitch(string), yaw(string)]
        buttons pipe:   integer: btn3 (bit2) | btn2 (bit1) | btn1 (bit0)
        accelerations:  list[x(float), y(float), z(float)]
        voice:          Transcript(list[Candidate(confidence: str, text: str)], threshold: int)

        Args:
            tacti (str)                     : "RIGHT" or "LEFT"
            pipe_name (TGear_Pipes_Name)    : enumeration of availables pipes

        Returns:
            a standard multiprocessing.Pipe class (from multiprocessing module)
        '''

        if pipe_name == TGear_Pipes_Name.GEST:
            return self.pipes[tacti].gesture_rx

        if pipe_name == TGear_Pipes_Name.ANGLE:
            return self.pipes[tacti].angle_rx

        if pipe_name == TGear_Pipes_Name.ACC:
            return self.pipes[tacti].acc_rx

        if pipe_name == TGear_Pipes_Name.BUTTON:
            return self.pipes[tacti].button_rx

        if pipe_name == TGear_Pipes_Name.VOICE:
            return self.pipes[tacti].voice_rx

    def select_sensors(self, tacti: str):
        '''
        Select stream of accelerometer, gyroscope, magnetomether data from Tactigon Skin.

        Args:
            tacti (str)                     : "RIGHT" or "LEFT"
        Returns:
            none
        '''
        if self.ble_process[tacti]:
            self.ble_process[tacti].select_sensors()  # type: ignore

    def select_voice(self, tacti):
        '''
        Select stream of microphone data from Tactigon Skin.

        Args:
            tacti (str)                     : "RIGHT" or "LEFT"
        Returns:
            none
        '''

        if self.ble_process[tacti]:
            self.ble_process[tacti].select_voice()  # type: ignore

    def start(self):
        '''
        Starts the engine

        Args:
            none
        
        Returns:
            none            
        '''

        if self.debug:
            print("TGear Engine started")

        devices = ["RIGHT", "LEFT"]
        for dev in devices:
            if self.enables[dev] == True:
                # start BLE
                if self.ble_process[dev]:
                    self.ble_process[dev].start()  # type: ignore
                # start GEST
                if self.gest_processes[dev]:
                    self.gest_processes[dev].start()  # type: ignore
                # start VOICE 
                if self.voice_processes[dev]:
                    self.voice_processes[dev].start()  # type: ignore

    def connection_status(self):
        '''
        Get the connection status of the devices.
        Returns one of TGear_Connection_Status values.
            - TGear_Connection_Status.NOT_INITIALIZED   : device is not initialized (should not check for connections here)
            - TGear_Connection_Status.CONNECTED         : device is connected
            - TGear_Connection_Status.DISCONNECTED      : device is not connected

        Args:
            none
        
        Returns:
            Tuple(left_tskin_connection_status, right_tskin_connection_status)
        '''

        l_conn_status = TGear_Connection_Status.NOT_INITIALIZED
        if self.ble_process["LEFT"]:
            if self.ble_process["LEFT"].get_connection_status():
                l_conn_status = TGear_Connection_Status.CONNECTED
            else:
                l_conn_status = TGear_Connection_Status.DISCONNECTED

        r_conn_status = TGear_Connection_Status.NOT_INITIALIZED
        if self.ble_process["RIGHT"]:
            if self.ble_process["RIGHT"].get_connection_status():
                r_conn_status = TGear_Connection_Status.CONNECTED
            else:
                r_conn_status = TGear_Connection_Status.DISCONNECTED

        return (l_conn_status, r_conn_status)

    def stop(self):
        '''
        Stops the engine - It's an alias for terminate

        Args:
            none
        
        Returns:
            none            
        '''
        self.terminate()

    def terminate(self):
        '''
        Terminates the engine: it disconnects from TSkins and terminates all processes

        Args:
            none
        
        Returns:
            none            
        '''

        if self.debug:
            print("TGear Engine teminated")

        devices = ["RIGHT", "LEFT"]
        for dev in devices:
            # stop BLE
            if self.ble_process[dev]:
                self.ble_process[dev].terminate() # type: ignore
            # stop GEST
            if self.gest_processes[dev]:
                self.gest_processes[dev].terminate() # type: ignore

            if self.voice_processes[dev]:
                self.voice_processes[dev].terminate() # type: ignore
