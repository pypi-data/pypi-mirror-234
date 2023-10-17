from enum import Enum
from dataclasses import dataclass, field
from multiprocessing.connection import PipeConnection
from os import path

from typing import Optional, Any, List, Union

@dataclass
class ConfigBase:
    base_path: str

@dataclass
class HAL:
    SERIAL_COM_PORT: str
    NUM_SAMPLE: int
    
    BLE_RIGHT_ADDRESS: str
    BLE_RIGHT_NAME: str
    BLE_RIGHT_ENABLE: bool
    
    BLE_LEFT_ADDRESS: str
    BLE_LEFT_NAME: str
    BLE_LEFT_ENABLE: bool

    INTERFACE: str = "Bluetooth"

    @classmethod
    def FromJSON(cls, json: dict):
        return cls(**json)

@dataclass
class RealTimeConfig(ConfigBase):
    MODEL_NAME_RIGHT: str = ""
    MODEL_NAME_LEFT: str = ""
    MODEL_PATH: str = "data/models"

    @property
    def model_full_path(self) -> str:
        return path.join(self.base_path, self.MODEL_PATH)

    @classmethod
    def FromJSON(cls, base_path: str, json: dict):
        return cls(base_path, **json)

@dataclass
class ClientConfig(ConfigBase):
    MODEL_NAME: str

    SERVER_URL: str = "https://tgear.eu.pythonanywhere.com"
    MODEL_GESTURES: List[str] = field(default_factory=list)
    MODEL_SPLIT_RATIO: float = 0.3
    MODEL_DATA_PATH: str = "data/models/"
    MODEL_SESSIONS: List[str] = field(default_factory=list)

    TRAINING_SESSIONS: List[str] = field(default_factory=list)

    @property
    def model_data_full_path(self):
        return path.join(self.base_path, self.MODEL_DATA_PATH, self.MODEL_NAME)
    
    @classmethod
    def FromJSON(cls, base_path, json):
        return cls(base_path, **json)

@dataclass
class UserData:
    user_id: str
    auth_key: str

    @classmethod
    def FromJSON(cls, json):
        return cls(**json)
    
@dataclass
class DataCollectionConfig(ConfigBase):
    SESSION_INFO: str
    HAND: str
    RAW_DATA_PATH: str = "data/raw"
    GESTURE_NAME: List[str] = field(default_factory=list)

    @property
    def raw_data_full_path(self) -> str:
        return path.join(self.base_path, self.RAW_DATA_PATH)

    @classmethod
    def FromJSON(cls, base_path: str, json: dict):
        return cls(base_path, **json)

class TSpeech_Version(Enum):
    OLD = 0
    NEW = 1

def get_or_default(json: dict, name: str, default):
    try:
        return json[name]
    except:
        return default

class AudioSource(Enum):
    MIC = 1
    TSKIN = 2

@dataclass
class HotWord:
    word: str
    boost: int = 1

    @classmethod
    def from_config(cls, config):
        return cls(config["word"], config["boost"])

class TSpeech:
    hotwords: List[HotWord]
    children: Optional["TSpeechObject"]

    def __init__(self, hotwords: Union[List[HotWord], HotWord], children: Optional["TSpeechObject"] = None):
        self.hotwords = hotwords if isinstance(hotwords, list) else [hotwords]
        self.children = children

    @classmethod
    def fromJSON(cls, json_obj, feedback_audio_path = ""):
        try:
            children = json_obj["children"]
        except:
            children = None

        return cls(
            [HotWord(hw) for hw in json_obj["hotwords"]],
            children=TSpeechObject.fromJSON(children, feedback_audio_path) if children else None,
        )

    @property
    def has_children(self):
        return self.children

    def __str__(self):
        return F"hotword: {self.hotwords}"

class TSpeechCommandEnum(Enum):
    LISTEN = 1
    STOP = 2
    PLAY = 3
    END = 99

class TSpeechObject:
    t_speech: List[TSpeech]
    feedback: str

    def __init__(self, t_speech: List[TSpeech], feedback: str = ""):
        self.t_speech = t_speech
        self.feedback = feedback

    @classmethod
    def fromJSON(cls, json_obj, feedback_audio_path = ""):

        try:
            feedback = path.join(feedback_audio_path, json_obj["feedback"])
        except:
            feedback = ""

        return cls(
            [TSpeech.fromJSON(t, feedback_audio_path) for t in json_obj["t_speech"]],
            feedback=feedback
        )

@dataclass
class TSpeechCommand:
    command_type: TSpeechCommandEnum
    speech_tree: Optional[TSpeechObject] = None
    audio_file: Optional[str] = None
    ack: bool = False

    @classmethod
    def listen(cls, speech_tree: TSpeechObject):
        return cls(
            TSpeechCommandEnum.LISTEN,
            speech_tree=speech_tree
        )

    @classmethod
    def play(cls, audio_file: str):
        return cls(
            TSpeechCommandEnum.PLAY,
            audio_file=audio_file
        )

    @classmethod
    def stop(cls):
        return cls(
            TSpeechCommandEnum.STOP
        )

    @classmethod
    def end(cls):
        return cls(
            TSpeechCommandEnum.END
        )

    # @classmethod
    # def fromJSON(cls, command_type, json_obj):
    #     if command_type == TSpeechCommandEnum.LISTEN:
    #         return cls.listen(
    #             [TSpeech() for ts in json_obj["parameter"]]
    #         )
    #     elif command_type == TSpeechCommandEnum.PLAY:
    #         return cls.play()
    #     elif command_type == TSpeechCommandEnum.STOP:
    #         return cls.stop()
    #     elif command_type == TSpeechCommandEnum.END:
    #         return cls.end()

    def set_ack(self):
        self.ack = True

    def is_completed(self):
        return self.ack

class Phrase:
    def __init__(self,
        hot_words: List[HotWord],
        phrase: str = "",
        gestures: List[List[str]] = [],
        timeout: int = 5,
        payload: Optional[Any] = None,
        audio_feedback: Optional[str] = None,
        error_feedback: Optional[str] = None,
        is_default: bool = False
    ):
        self.hot_words = hot_words
        self.phrase = phrase
        self.gestures = gestures
        self.timeout = timeout
        self.payload = payload
        self.audio_feedback = audio_feedback
        self.error_feedback = error_feedback
        self.is_default = is_default

    @classmethod
    def from_config(cls, config):
        try:
            gestures = config["gestures"]
        except:
            gestures = []

        try:
            phrase = config["phrase"]
        except:
            phrase = ""

        return Phrase(
            hot_words=[HotWord.from_config(hw) for hw in config["hot_words"]],
            gestures=gestures,
            timeout=config["timeout"],
            audio_feedback=config["audio_feedback"],
            error_feedback=config["error_feedback"],
            is_default=config["is_default"],
            payload=config["payload"],
            phrase=phrase,
            )

    def __str__(self):
        return F"{self.hot_words} | is default: {self.is_default}"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Phrase):
            return self.hot_words == __o.hot_words

        return False

class Candidate_Transcript_Message:
    """Contains a candidate for the voice recognition routine and it's confidence score
    """
    def __init__(self, confidence: float, text: str):
        self.confidence = confidence
        self.text = text

    def __str__(self):
        return self.text + ": " + str(round(self.confidence, 2))
        # return F"Candidate[confidence: {self.confidence}, text: {self.text}]"

    @classmethod
    def from_metadata(cls, metadata):
        return cls(metadata.confidence, "".join([token.text for token in metadata.tokens]))

    @property
    def as_list(self):
        return self.text.split(" ")

    def __contains__(self, to_find: str):
        return to_find in self.text

class Transcripts_Message:
    """ Contains all the candidates from the voice recognition routine and the threshold value that has been set
    """
    def __init__(self, candidate: List[Candidate_Transcript_Message], threshold: int):
        self.candidate = candidate
        self.threshold = threshold
        self.confidence = -100

        self.get_transcripts_confidence()

    @classmethod
    def from_metadata(cls, metadata, threshold: int):
        return cls([Candidate_Transcript_Message.from_metadata(transcript) for transcript in metadata.transcripts], threshold)

    def __contains__(self, word: str):
        return len(self.get_candidate_containig(word)) > 0

    def get_transcripts_confidence(self):
        l = [c.confidence for c in self.candidate if c.confidence > 0]
        if len(l) > 0:
            self.confidence = sum(l) / len(l)

    def get_candidate_containig(self, to_find: str):
        return [c for c in self.candidate if to_find in c]

    def get_all_valid(self):
        return [c for c in self.candidate if c.confidence > self.threshold]

    def check_against_hotwords(self, hot_words):
        found = []
        score = len(hot_words)
        # if len(hot_words) > 1:
        #     score = len(hot_words)//2
        # else:
        #     score = 1
        for hw in hot_words:
            for c in self.candidate:
                if hw in c.as_list and not hw in found:
                    found.append(hw)
                    if len(found)/score >= 0.5:
                        return True

        return False
    
    def get_first_valid(self):
        return next(filter(lambda c : c.confidence > self.threshold, self.candidate), None)

    def dump(self):
        for i, c in enumerate(self.candidate):
            print(F"{c} {i}/{len(self.candidate)}")

    def __str__(self):
        return F"{str([str(c) for c in self.candidate])}"

@dataclass
class Voice(ConfigBase):
    model: str
    audio_source: AudioSource = AudioSource.MIC
    scorer: Optional[str] = None

    vad_aggressiveness: int = 3
    vad_padding_ms: int = 800
    vad_ratio: float = 0.6
    beam_width: int = 1024

    min_sample_len: int = 180

    voice_timeout: int = 10
    silence_timeout: int = 5

    audio_file_location: str = ""
    num_transcript: int = 10
    default_phrases: List[Any] = field(default_factory=list)

    stop_hotword: HotWord = HotWord("exit")
    tactigon_speech_version: TSpeech_Version = TSpeech_Version.NEW

    @property
    def model_full_path(self) -> str:
        return path.join(self.base_path, self.model)
    
    @property
    def scorer_full_path(self) -> Optional[str]:
        if self.scorer is None:
            return None
        
        return path.join(self.base_path, self.scorer)

    @classmethod
    def FromJSON(cls, base_path: str, json: dict):
        return cls(
            base_path,
            json["model"],
            AudioSource(get_or_default(json, "audio_source", cls.audio_source.value)),
            get_or_default(json, "scorer", cls.scorer),
            get_or_default(json, "vad_aggressiveness", cls.vad_aggressiveness),
            get_or_default(json, "vad_padding_ms", cls.vad_padding_ms),
            get_or_default(json, "vad_ratio", cls.vad_ratio),
            get_or_default(json, "beam_width", cls.beam_width),
            get_or_default(json, "min_sample_len", cls.min_sample_len),
            get_or_default(json, "voice_timeout", cls.voice_timeout),
            get_or_default(json, "silence_timeout", cls.silence_timeout),
            get_or_default(json, "audio_file_location", cls.audio_file_location),
            get_or_default(json, "num_transcript", cls.num_transcript),
            get_or_default(json, "default_phrases", []),
        )


class TBleConnectionStatus(Enum):
    NONE = 0
    CONNECTING = 1
    CONNECTED = 2
    DISCONNECTING = 3
    DISCONNECTED = 4

class TBleSelector(Enum):
    NONE = 0
    SENSORS = 1
    VOICE = 2

class TGear_Pipes_Name(Enum):
    GEST = 1,           'gesture pipe enumeration'
    ANGLE = 2,          'Eulero angles pipe enumeration'
    ACC = 3,            'xyz accelerations pipe enumeration'
    BUTTON = 4,         'buttons pipe enumeration'
    VOICE = 5,          'voice pipe enumeration'


class TGear_Connection_Status(Enum):
    NOT_INITIALIZED = 0,
    CONNECTED = 1,
    DISCONNECTED = 2,


class Pipes:
    sensor_tx: Optional[PipeConnection] = None 
    sensor_rx: Optional[PipeConnection] = None
    adpcm_tx: Optional[PipeConnection] = None
    adpcm_rx: Optional[PipeConnection] = None

    gesture_tx = gesture_rx = False
    angle_tx = angle_rx = False
    acc_tx = acc_rx = False
    button_tx = button_rx = False
    voice_tx = voice_rx = False

# class _BLEProcess:
#     right: Optional[BLE]
#     left: Optional[BLE]
