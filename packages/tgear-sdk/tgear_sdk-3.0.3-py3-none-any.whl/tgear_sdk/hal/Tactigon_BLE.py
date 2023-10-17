import asyncio
from bleak import BleakClient
import struct
import time
import math

from multiprocessing import Process, Value
from multiprocessing.connection import PipeConnection
from multiprocessing.sharedctypes import Synchronized
from typing import Optional

from blue_st_sdk.features.audio.adpcm.feature_audio_adpcm import FeatureAudioADPCM
from ..models import TBleConnectionStatus, TBleSelector


class TBle:
    SENSORS_UUID: str = "bea5760d-503d-4920-b000-101e7306b005"
    VOICE_DATA_UUID = "08000000-0001-11e1-ac36-0002a5d5c51b"
    VOICE_SYNCH_UUID = "40000000-0001-11e1-ac36-0002a5d5c51b"

    name: str
    ble_address: str
    acc_pipe: Optional[PipeConnection] = None
    angle_pipe: Optional[PipeConnection] = None
    button_pipe: Optional[PipeConnection] = None
    adpcm_pipe: Optional[PipeConnection] = None
    
    connection_status: Optional[Synchronized] = None
    is_running: Optional[Synchronized] = None
    selector: Optional[Synchronized] = None

    accX: float
    accY: float
    accZ: float

    gyroX: float
    gyroY: float
    gyroZ: float

    roll: float
    pitch: float
    yaw: float

    button: int

    def __init__(self,
                 name: str, 
                 ble_address: str, 
                 sensor_pipe: Optional[PipeConnection] = None, 
                 acc_pipe: Optional[PipeConnection] = None, 
                 angle_pipe: Optional[PipeConnection] = None, 
                 button_pipe: Optional[PipeConnection] = None, 
                 adpcm_pipe: Optional[PipeConnection] = None,
                 connection_status: Optional[Synchronized] = None,
                 is_running: Optional[Synchronized] = None,
                 selector: Optional[Synchronized] = None,
                 debug: bool = False,
                 ):
        self.debug = debug

        self.name = name
        self.ble_address = ble_address
        self.sensor_pipe = sensor_pipe
        self.acc_pipe = acc_pipe
        self.angle_pipe = angle_pipe
        self.button_pipe = button_pipe
        self.adpcm_pipe = adpcm_pipe
        self.connection_status = connection_status
        self.is_running = is_running

        self.adpcm_audio = FeatureAudioADPCM(None)
        
        self.selector = selector

        self.loop = asyncio.get_event_loop()
        main_task = self.loop.create_task(self.run())
        self.loop.run_until_complete(main_task)

    async def run(self):

        def handle_voice(char, data: bytearray):
            audio = self.adpcm_audio.extract_data(0, data, 0)
            if self.adpcm_pipe:
                self.adpcm_pipe.send(audio.get_sample().get_data())

        def handle_sensors(char, data:bytearray):
            self.accX = float(struct.unpack("h", bytes(data[0:2]))[0])
            self.accY = float(struct.unpack("h", bytes(data[2:4]))[0])
            self.accZ = float(struct.unpack("h", bytes(data[4:6]))[0])
            
            self.gyroX = float(struct.unpack("h", bytes(data[6:8]))[0])
            self.gyroY = float(struct.unpack("h", bytes(data[8:10]))[0])
            self.gyroZ = float(struct.unpack("h", bytes(data[10:12]))[0])
            
            self.roll = float(struct.unpack("h", bytes(data[12:14]))[0])
            self.pitch = float(struct.unpack("h", bytes(data[14:16]))[0])
            self.yaw = float(struct.unpack("h", bytes(data[16:18]))[0])
            
            try:
                self.button = int(struct.unpack("h", bytes(data[18:20]))[0])
            except:
                pass

            self.gravity_comp()

            if self.sensor_pipe:
                self.sensor_pipe.send(
                    [
                        self.accX,
                        self.accY,
                        self.accZ,
                        self.gyroX,
                        self.gyroY,
                        self.gyroZ,
                    ]
                )

            if self.acc_pipe:
                self.acc_pipe.send([self.accX, self.accY, self.accZ])

            if self.angle_pipe:
                self.angle_pipe.send([self.roll, self.pitch, self.yaw])
            try:
                if self.button_pipe:
                    self.button_pipe.send([self.button])
            except:
                pass
            
            if self.debug:
                print(self.accX,self.accY,self.accZ,self.gyroX, self.gyroY,self.gyroZ,self.roll,self.pitch,self.yaw,self.button)

        if self.is_running is None:
            raise Exception("is_running parameter should be a multiprocessing.Value")
        
        if self.connection_status is None:
            raise Exception("connection_status parameter should be a multiprocessing.Value")
        
        if self.selector is None:
            raise Exception("selector parameter should be a multiprocessing.Value")

        run: bool = True
        current_selector = None
        client = None

        is_notifying_sensors: bool = False
        is_notifying_voice: bool = False

        while run:
            self.connection_status.value = TBleConnectionStatus.CONNECTING.value
            try:
                print("Connecting to", self.name, "BLE", self.ble_address)
                client = BleakClient(self.ble_address)
                await client.connect()
                self.connection_status.value = TBleConnectionStatus.CONNECTED.value
                current_selector = None
                is_notifying_sensors = False
                is_notifying_voice = False
                print("Tactigon", self.name, "BLE", self.ble_address, "connected!")
            except:
                client = None
                print("Tactigon", self.name, "BLE", self.ble_address, "not detected...")
                time.sleep(5)
                continue

            
            while client.is_connected:
                if not self.is_running.value:
                    self.connection_status.value = TBleConnectionStatus.DISCONNECTING.value
                    await client.disconnect()
                    self.connection_status.value = TBleConnectionStatus.DISCONNECTED.value
                    run = False
                    break

                if current_selector != self.selector.value:
                    current_selector = self.selector.value

                    if is_notifying_sensors:
                        await client.stop_notify(self.SENSORS_UUID)
                        is_notifying_sensors = False
                    if is_notifying_voice:
                        await client.stop_notify(self.VOICE_DATA_UUID)
                        await client.stop_notify(self.VOICE_SYNCH_UUID)
                        is_notifying_voice = False
                    
                    if current_selector == TBleSelector.SENSORS.value:
                        if client.is_connected:
                            
                            await client.start_notify(self.SENSORS_UUID, handle_sensors)
                            is_notifying_sensors = True

                    elif current_selector == TBleSelector.VOICE.value:
                        if client.is_connected:
                            await client.start_notify(self.VOICE_SYNCH_UUID, lambda c, d: None)
                            await client.start_notify(self.VOICE_DATA_UUID, handle_voice)
                            is_notifying_voice = True
                else:
                    await asyncio.sleep(0.02)
        if client:
            await client.disconnect()
            print("Disconnected")

        print("Stopped BLE process for", self.name, self.ble_address)

    def gravity_comp(self):
        """gravity compensation"""
        G_CONST = 9.81
        ANG_TO_RAD = math.pi / 180
        ACC_RATIO = 1000
        VEL_RATIO = 30

        if self.name == "LEFT":
            self.accX = -self.accX / ACC_RATIO
            self.accY = -self.accY / ACC_RATIO
            self.accZ = -self.accZ / ACC_RATIO

            self.gyroX = -self.gyroX / VEL_RATIO
            self.gyroY = -self.gyroY / VEL_RATIO
            self.gyroZ = -self.gyroZ / VEL_RATIO

        else:
            self.accX = self.accX / ACC_RATIO
            self.accY = self.accY / ACC_RATIO
            self.accZ = -self.accZ / ACC_RATIO

            self.gyroX = self.gyroX / VEL_RATIO
            self.gyroY = self.gyroY / VEL_RATIO
            self.gyroZ = -self.gyroZ / VEL_RATIO

        if self.name == "LEFT":
            pitch = self.roll * ANG_TO_RAD
            roll = self.pitch * ANG_TO_RAD
        else:
            pitch = -self.roll * ANG_TO_RAD
            roll = -self.pitch * ANG_TO_RAD

        if self.accZ == 0:
            beta = math.pi / 2
        else:
            beta = math.atan(
                math.sqrt(math.pow(self.accX, 2) + math.pow(self.accY, 2)) / self.accZ
            )

        self.accX = self.accX - G_CONST * math.sin(roll)
        self.accY = self.accY + G_CONST * math.sin(pitch)
        self.accZ = self.accZ - G_CONST * math.cos(beta)   

class BLE:
    is_running: Synchronized
    connection_status: Synchronized
    selector: Synchronized

    def __init__(self, 
                 name: str, 
                 ble_address: str, 
                 sensor_pipe: Optional[PipeConnection] = None, 
                 acc_pipe: Optional[PipeConnection] = None, 
                 angle_pipe: Optional[PipeConnection] = None, 
                 button_pipe: Optional[PipeConnection] = None, 
                 adpcm_pipe: Optional[PipeConnection] = None,
                 debug: bool = False):

        self.connection_status = Value("b", TBleConnectionStatus.NONE.value) # type: ignore
        self.is_running = Value("b", True) # type: ignore
        self.selector = Value("b", TBleSelector.SENSORS.value) # type: ignore
        self.process = Process(
            target=TBle,
            args=(
                name,
                ble_address,
                sensor_pipe,
                acc_pipe,
                angle_pipe,
                button_pipe,
                adpcm_pipe,
                self.connection_status,
                self.is_running,
                self.selector,
                debug)
            )

    def start(self):
        self.process.start()

    def terminate(self):
        self.is_running.value = False
        self.process.join(20)
        self.process.terminate()

    def select_sensors(self):
        self.selector.value = TBleSelector.SENSORS.value

    def select_voice(self):
        self.selector.value = TBleSelector.VOICE.value

    def select(self, selector: TBleSelector = TBleSelector.NONE):
        self.selector.value = selector.value

    def get_connection_status(self):
        return self.connection_status.value == TBleConnectionStatus.CONNECTED.value

# import wave
# from blue_st_sdk.utils.number_conversion import LittleEndian
# from multiprocessing import Pipe
# from webrtcvad import Vad

# class TAudio:
#     sample_rate: int = 16000
#     frame_duration: int = 20
#     tskin_frame_length: int = 80 // 2

#     buffer_per_seconds: int = 400

#     def __init__(self, in_pipe: PipeConnection):
#         self.frame_buffer_length = self.sample_rate * self.frame_duration // 1000 // self.tskin_frame_length
#         self.in_pipe = in_pipe

#         num_seconds = 5
#         length = self.buffer_per_seconds // self.frame_buffer_length * num_seconds

#         self.buffer_queue = queue.Queue(maxsize=length)
#         self.vad = Vad(3)

#         while not self.in_pipe.poll():
#             time.sleep(0.5)

#         n_buffer = 0
#         data = b''
#         while self.in_pipe.poll(0.5):
#             data += b''.join([LittleEndian.int16_to_bytes(d) for d in self.in_pipe.recv()])
#             n_buffer += 1

#             if not n_buffer < self.frame_buffer_length:
#                 self.buffer_queue.put(data)
#                 data = b''
#                 n_buffer = 0
#                 print(self.buffer_queue.qsize(), length)
#             if self.buffer_queue.full():
#                 break

#         wf = wave.open("vad.wav", "w")
#         wf.setnchannels(1)
#         wf.setsampwidth(2)
#         wf.setframerate(self.sample_rate)

#         w2 = wave.open("check.wav", "w")
#         w2.setnchannels(1)
#         w2.setsampwidth(2)
#         w2.setframerate(self.sample_rate)

#         while self.buffer_queue.qsize() != 0:
#             f = self.buffer_queue.get()
#             w2.writeframes(f)
#             if self.vad.is_speech(f, self.sample_rate):
#                 wf.writeframes(f)


#             # self.frame_buffer.put(self.in_pipe.recv())

#             # if self.frame_buffer.full():
#             #     data = b''
#             #     while not self.frame_buffer.empty():
#             #         data += b''.join([LittleEndian.int16_to_bytes(d) for d in self.frame_buffer.get()])
                
#             #     if self.vad.is_speech(data, self.sample_rate):
#             #         wf.writeframes(data)
#             #         self.buffer_queue.put(data)
#         w2.close()
#         wf.close()

#     def read(self):
#         """Return a block of audio data, blocking if necessary."""
#         return self.buffer_queue.get()

# def debug():
#     pipe_r, pipe_t = Pipe(duplex=False)
#     ble = BLE("TEST", "C0:83:38:32:55:36", adpcm_pipe=pipe_t)
#     ble.select_voice()
#     ble.start()
#     taudio = Process(target=TAudio, args=(pipe_r,))
#     taudio.start()
#     taudio.join()
#     ble.terminate()


# if __name__ == "__main__":
#     debug()