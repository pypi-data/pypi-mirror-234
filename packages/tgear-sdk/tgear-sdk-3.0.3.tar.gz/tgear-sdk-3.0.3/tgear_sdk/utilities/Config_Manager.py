import json
# import sys
from os import path

# resource directory - need to be referenced to exe path when used with exe bundle
# if getattr(sys, "frozen", False):
#     CONFIG_FILES_DIR = path.join(sys._MEIPASS, "./config_files")
#     CLIENT_PY_PATH = sys._MEIPASS
# else:
#     CONFIG_FILES_DIR = path.join(path.dirname(__file__), "../config_files")
#     CLIENT_PY_PATH = path.join(path.dirname(__file__), "../")

CONFIG_FILES_DIR = path.join(path.dirname(__file__), "../config_files")
CLIENT_PY_PATH = path.join(path.dirname(__file__), "../")

class Config_Manager:
    """
    The configuration manager class is responsible for reading, parsing and accessing configuration files.
    """

    def __init__(self, config):
        self.config = config

    @classmethod
    def from_file(cls, name):
        """
        This method return config_files object by loading the json file
        :param name: config_files file name without extension
        :return: config_files object
        """
        if not name.endswith(".json"):
            name = name + ".json"

        with open(path.join(CONFIG_FILES_DIR, name)) as config_file:
            return cls(json.load(config_file))

    def get(self, name):
        """:return: json name value"""
        return self.config.get(name, "")

def config_files_checks():

    # model file
    rt_config = Config_Manager.from_file("real_time.json")
    model_path = rt_config.get("MODEL_PATH")

    hal_config = Config_Manager.from_file("hal.json")

    if hal_config.get("BLE_RIGHT_ENABLE"):

        model_name = rt_config.get("MODEL_NAME_RIGHT")
        right_model_path = path.join(
            CLIENT_PY_PATH, model_path, model_name, "model.pickle"
        )

        if not path.exists(right_model_path):
            print("Invalid Right Hand model, check real_time.json file")
            return False

    if hal_config.get("BLE_LEFT_ENABLE"):

        model_name = rt_config.get("MODEL_NAME_LEFT")
        left_model_path = path.join(
            CLIENT_PY_PATH, model_path, model_name, "model.pickle"
        )

        if not path.exists(left_model_path):
            print("Invalid Left Hand model, check real_time.json file")
            return False

    return True


# Start point of the application
if __name__ == "__main__":

    hal_config = Config_Manager.from_file("apps/application_gesture_to_ui.json")

    combo = hal_config.get("COMBO_2")
    print(combo["combo_gestures"])

    input("type any key")