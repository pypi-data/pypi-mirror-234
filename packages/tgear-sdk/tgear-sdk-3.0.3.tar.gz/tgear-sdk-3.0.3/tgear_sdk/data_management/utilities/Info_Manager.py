import sys
import os
import pandas as pd
from os import path
from numpy import row_stack

# resource directory - need to be referenced to exe path when used with exe bundle
# if getattr(sys, "frozen", False):
#     CLIENT_PY_PATH = sys._MEIPASS
# else:
#     CLIENT_PY_PATH = path.join(path.dirname(__file__), "../../")
#     sys.path.insert(0, path.join(CLIENT_PY_PATH, "utilities"))

# sys.path.insert(0, path.join(CLIENT_PY_PATH, "utilities"))
# from Config_Manager import Config_Manager

# CLIENT_PY_PATH = path.join(path.dirname(__file__), "../../")
# from ...utilities.Config_Manager import Config_Manager

from ...models import DataCollectionConfig, UserData, HAL

def load_info(user_data: UserData, data_collection_config: DataCollectionConfig, hal: HAL):
    """
    This function load info files and update info dataframes with config file values
    :param config: config object of data collection
    :return: person, gesture, and session dataframes
    """
    # import json config
    # dc_config = Config_Manager.from_file("data_collection.json")
    # user_config = Config_Manager.from_file("user_data.json")
    # hal_config = Config_Manager.from_file("hal.json")

    # raw_data_path = path.join(CLIENT_PY_PATH, dc_config.get("RAW_DATA_PATH"))

    path_person = data_collection_config.raw_data_full_path + "info/person.csv"
    path_gesture = data_collection_config.raw_data_full_path + "info/gesture.csv"
    path_session = data_collection_config.raw_data_full_path + "info/session.csv"
    path_device = data_collection_config.raw_data_full_path + "info/device.csv"

    ## If info file doesn't exists then create new info file with data
    ## otherwise load the already existing info
    if not os.path.exists(path_person):
        person_data = pd.DataFrame(columns=["person_name"])
        person_data.to_csv(path_person)
    else:
        person_data = pd.read_csv(path_person, index_col=0)

    if not os.path.exists(path_gesture):
        gestures_data = pd.DataFrame(columns=["gesture_names"])
        gestures_data.to_csv(path_gesture)
    else:
        gestures_data = pd.read_csv(path_gesture, index_col=0)

    if not os.path.exists(path_session):
        session_data = pd.DataFrame(columns=["session_info"])
        session_data.to_csv(path_session)
    else:
        session_data = pd.read_csv(path_session, index_col=0)   

    if not os.path.exists(path_device):
        device_data = pd.DataFrame(columns=["dev_id"])
        device_data.to_csv(path_device)
    else:
        device_data = pd.read_csv(path_device, index_col=0)       

    ## get device info
    if hal.INTERFACE == "Bluetooth":      
        if data_collection_config.HAND == "RIGHT":
            b_add = hal.BLE_RIGHT_ADDRESS
        else:
            b_add = hal.BLE_LEFT_ADDRESS
    else:
        b_add = "serial"


    return person_data, gestures_data, session_data, device_data





def update_dataframe(df, column, value):
    """
    This function update dataframe given column name and value if that values doesn't exist
    :param df: dataframe
    :param column: name of the column
    :param value: list of values
    :return: updated dataframe
    """
    for v in value:
        if get_index(df, column, v) == "":
            df.loc[len(df)] = v
    return df

def update_dataframe_2D___unused(df, column_1, column_2, value_1, value_2):

    for idx in df[df[column_1] == value_1].index.tolist():
        if idx in df[df[column_2] == value_2].index.tolist():
            # already exists
            return df
    
    df.loc[len(df)] = [value_1,value_2]
    return df

        


def update_info(raw_data_path, person_data, gesture_data, session_data, device_data):
    """
    This function save dataframes as csv file
    :param raw_data_path: path of the raw data folder
    :param person_data: dataframe with person info
    :param gesture_data: dataframe with gesture info
    :param session_data: dataframe with session info
    :return: none
    """

    person_data.to_csv(raw_data_path + "info/person.csv")
    gesture_data.to_csv(raw_data_path + "info/gesture.csv")
    session_data.to_csv(raw_data_path + "info/session.csv")
    device_data.to_csv(raw_data_path + "info/device.csv")
    print("data saved as csv\n\n")


def get_index(df, column, data):
    """
    Function returns the index of the row for a column value
    :param df: dataframe
    :param column: name of the column
    :param data: value you are searching
    :return: index of the row
    """
    idx = df[df[column] == data].index.tolist()
    idx = str(idx).replace("[", "")
    idx = idx.replace("]", "")
    return idx


def get_value(df, column, row_idx):
    """
    Function returns the value @ column/row_idx
    :param df: dataframe
    :param column: name of the column
    :row_idx: index of the row (starting from 0)
    :return: value @ column/row_idx
    """
    try:
        return df[column][row_idx]
    except:
        return None
