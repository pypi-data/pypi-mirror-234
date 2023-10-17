import json
import time 

from os import path
from datetime import datetime
from tgear_sdk import TGear_Engine, TGear_Connection_Status
from tgear_sdk.models import HAL, RealTimeConfig, Voice, TGear_Pipes_Name, TSpeechObject, TSpeechCommand, TSpeech, HotWord, AudioSource

def test_tree(tree, voice_pipe, stop_word):

    voice_pipe.send(
        TSpeechCommand.listen(tree)
    )

    if not voice_pipe.poll(20):
        voice_pipe.send(
            TSpeechCommand.stop()
        )
        return [None]

    result = voice_pipe.recv()
    
    if type(result) == TimeoutError:
        # print("voice timeout")
        return []

    transcript, tree_path, inference = result

    if tree_path and tree_path[-1] == stop_word:
        # print("stop word, esco")
        return [None]

    filtered_tree = filter_tree(tree, tree_path)

    if filtered_tree:
        print("Ho capito", tree_path)
        print("Mi mancano le seguenti possibilità")

        for b in filtered_tree.t_speech:
            for hw in b.hotwords:
                print("----" + hw.word)

        print("\nfeedback", filtered_tree.feedback)

        return tree_path + test_tree(filtered_tree, voice_pipe, stop_word)

    return tree_path

def filter_tree(tree, tree_path) -> TSpeechObject:
    if not tree_path:
        return tree

    print(tree_path)
    node, *rest = tree_path

    branches = [branch.children for branch in tree.t_speech if node in branch.hotwords]

    if not branches:
        return tree

    filtered_tree, *_ = branches

    if not filtered_tree:
        return tree

    return filter_tree(filtered_tree, rest)


class Test:

    tgear: TGear_Engine
    run: bool = True

    def __init__(self):
        base_path_data: str = path.join(path.dirname(__file__), "../../")
        base_path_voice: str = path.join(path.dirname(__file__), "../../config_files")

        with open(path.join(path.dirname(__file__), "../../config_files", "hal.json")) as hal_file:
            hal = HAL.FromJSON(json.load(hal_file))

        with open(path.join(path.dirname(__file__), "../../config_files", "real_time.json")) as real_time_file:
            real_time = RealTimeConfig.FromJSON(base_path_data, json.load(real_time_file))

        with open(path.join(path.dirname(__file__), "../../config_files", "voice.json")) as voice_file:
            voice = Voice.FromJSON(base_path_voice, json.load(voice_file))
        
        voice.audio_source = AudioSource.MIC

        self.tgear = TGear_Engine(hal, real_time, voice)
        self.tgear.config("RIGHT", gesture_pipe_en=True, angle_pipe_en=True, button_pipe_en=True, voice_pipe_en=True)

        self.gesture_pipe = self.tgear.get_pipe("RIGHT", TGear_Pipes_Name.GEST) # type: ignore
        self.button_pipe = self.tgear.get_pipe("RIGHT", TGear_Pipes_Name.BUTTON) # type: ignore
        self.voice_pipe = self.tgear.get_pipe("RIGHT", TGear_Pipes_Name.VOICE) # type: ignore
        self.angle_pipe = self.tgear.get_pipe("RIGHT", TGear_Pipes_Name.ANGLE) # type: ignore

    def start(self):

        TICK_PERIOD_MS = 100
        tick = datetime.now()

        g = None
        a = None
        b = None

        self.tgear.start()
        
        while True:
            tgear_conn_status = self.tgear.connection_status()
            if TGear_Connection_Status.CONNECTED in tgear_conn_status:
                break

            print("Waiting for TSkin(s) connection")
            time.sleep(1)

        while self.run:
            if self.gesture_pipe and self.gesture_pipe.poll(): # type: ignore
                g = self.gesture_pipe.recv() # type: ignore

            if self.angle_pipe and self.angle_pipe.poll(): # type: ignore
                a = self.angle_pipe.recv() # type: ignore

            if self.button_pipe and self.button_pipe.poll(): # type: ignore
                b = self.button_pipe.recv() # type: ignore

            delta = datetime.now() - tick

            if delta.total_seconds() < TICK_PERIOD_MS/1000:
                continue
        
            tick = datetime.now()

            print("gesture:", g, "| angle:", a, "| button:", b)

            if b == [1]:
                print("stop")
                self.run = False
            elif b == [4]:
                print("voice")
                self.tgear.select_voice("RIGHT")

                tree = test_tree(
                    TSpeechObject(
                        [TSpeech(
                            [HotWord("draw")],
                            children=TSpeechObject(
                                [
                                    TSpeech(
                                        [HotWord("circle")]
                                    ),
                                    TSpeech(
                                        [HotWord("cone")]
                                    ),
                                ]
                            )
                        )],
                        "draw"
                    )
                    , self.voice_pipe
                    , self.tgear.voice.stop_hotword
                )

                print(tree)

                print("stop voce")
                self.tgear.select_sensors("RIGHT")

            
            g = None
            a = None
            b = None
        
        self.tgear.stop()


if __name__ == "__main__":
    t = Test()
    t.start()