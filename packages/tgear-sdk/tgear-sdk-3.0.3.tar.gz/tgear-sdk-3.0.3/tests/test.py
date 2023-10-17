import json
from multiprocessing.connection import PipeConnection
from os import path
from typing import List
from tgear_sdk import TGear_Engine

from tgear_sdk.models import HAL, RealTimeConfig, Voice, TGear_Pipes_Name, AudioSource, TSpeechObject, TSpeechCommand, HotWord, TSpeech, TSpeech_Version, Phrase

def test_tree(tree: TSpeechObject, voice_pipe: PipeConnection, stop_word: HotWord):

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

def filter_tree(tree: TSpeechObject, tree_path: List[HotWord]) -> TSpeechObject:
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

def test_voice(button_pipe, voice_pipe, tgear):
    while True:
        if button_pipe.poll(0.5):
            button = button_pipe.recv()[0]

            if button == 4:
                print("start voce")
                
                voice_pipe.send(
                    TSpeechCommand.play("D:\\projects\\TSkin\\TGear_SDK\\src\\applications\\application_rhino\\voices\\command_ok.wav")
                )
                
                if voice_pipe.poll(10):
                    _ = voice_pipe.recv()

                tgear.select_voice("RIGHT")

                d = test_tree(
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
                    , voice_pipe
                    , tgear.voice.stop_hotword
                )

                print(d)

                print("stop voce")
                tgear.select_sensors("RIGHT")

                while button_pipe.poll():
                    _ = button_pipe.recv()

            if button == 1:
                print("Exit")
                break

def test_voice_old(voice_pipe):
    wake_up = Phrase([HotWord("draw"), HotWord("circle")], is_default=True, audio_feedback="how_can_i_help_you.wav")
    ph = [wake_up]

    teacher = Phrase([HotWord("teach"), HotWord("lesson")], audio_feedback="choose_a_lesson.wav", error_feedback="i_didnt_understand.wav")
    student = Phrase([HotWord("repeat"), HotWord("learn")], audio_feedback="choose_a_lesson.wav")
    exit_p = Phrase([HotWord("exit"), HotWord("program")], audio_feedback="exiting_program.wav")

    while True:
        voice_pipe.send(ph)
        while not voice_pipe.poll():
            pass

        res = voice_pipe.recv()
        print(res)

def test_gesture(gesture_pipe):
    while True:
        if gesture_pipe.poll():
            print(gesture_pipe.recv())

def test():
    pass

def test_app():
    base_path_data: str = path.join(path.dirname(__file__), "../../")
    base_path_voice: str = path.join(path.dirname(__file__), "../../config_files")

    with open(path.join(path.dirname(__file__), "../../config_files", "hal.json")) as hal_file:
        hal = HAL.FromJSON(json.load(hal_file))

    with open(path.join(path.dirname(__file__), "../../config_files", "real_time.json")) as real_time_file:
        real_time = RealTimeConfig.FromJSON(base_path_data, json.load(real_time_file))

    with open(path.join(path.dirname(__file__), "../../config_files", "voice.json")) as voice_file:
        voice = Voice.FromJSON(base_path_voice, json.load(voice_file))

    voice.audio_source = AudioSource.MIC

    t = TGear_Engine(hal, real_time, voice)
    t.config("RIGHT", gesture_pipe_en=True)
    # t.config("RIGHT", voice_pipe_en=True, button_pipe_en=True)

    gesture_pipe: PipeConnection = t.get_pipe("RIGHT", TGear_Pipes_Name.GEST) # type: ignore
    # voice_pipe: PipeConnection = t.get_pipe("RIGHT", TGear_Pipes_Name.VOICE) # type: ignore
    # button_pipe: PipeConnection = t.get_pipe("RIGHT", TGear_Pipes_Name.BUTTON) # type: ignore

    t.start()

    test()
    # test_gesture(gesture_pipe)
    # test_voice_old(voice_pipe)
        
    t.stop()

if __name__ == "__main__":
    test_app()