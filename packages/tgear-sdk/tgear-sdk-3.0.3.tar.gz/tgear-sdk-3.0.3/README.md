# Tactigon Gear SDK

![The tactigon team](https://avatars.githubusercontent.com/u/63020285?s=200&v=4)

This package enables the wearable device Tactigon Skin to connect to your python project using Bluetooth Low Energy.

SDK version: 3.0.2

## Content
- [Tactigon Gear SDK](#tactigon-gear-sdk)
  - [Content](#content)
  - [1. Architecture](#1-architecture)
  - [2. Prerequisites](#2-prerequisites)
  - [3. Licensing](#3-licensing)
  - [4. Tactigon Skin](#4-tactigon-skin)
    - [4.1. Status led](#41-status-led)
  - [5. Tactigon Gear SDK General example](#5-tactigon-gear-sdk-general-example)
  - [6. Tactigon Gear CLI instructions](#6-tactigon-gear-cli-instructions)
    - [6.1. Tactigon Gear CLI config files](#61-tactigon-gear-cli-config-files)
    - [6.2. Tactigon Gear CLI training session](#62-tactigon-gear-cli-training-session)
    - [6.3. Tactigon Gear CLI Training Data Upload](#63-tactigon-gear-cli-training-data-upload)
    - [6.4. Tactigon Gear CLI Model Building Instructions](#64-tactigon-gear-cli-model-building-instructions)
    - [6.5. Tactigon Gear CLI Model Download Instructions](#65-tactigon-gear-cli-model-download-instructions)
    - [6.6. Tactigon Gear CLI Gesture Recognition Setup and Test](#66-tactigon-gear-cli-gesture-recognition-setup-and-test)
- [Appendix](#appendix)


<div style="page-break-after: always;"></div>

##  1. <a name='Architecture'></a>Architecture

Tactigon Gear environment has the following architecture:

Server is located on the cloud and it is manteined by Next Industries s.r.l.
Server has a web interface where you can handle your profile and your data (models and gestures)

Provided Tactigon Gear SDK is the implementation of Tactigon Gear environment client side

Tactigon Gear SDK is used for collecting new raw data, send the data to server,
ask server to train a model using the raw data, and download the model from server. 
Finally use the model for testing real-time gesture recognition.

##  2. <a name='Prerequisites'></a>Prerequisites
In order to use the Tactigon Gear SDK the following prerequisites needs to be observed:

* Python version: following versions has been used and tested. It is STRONGLY recommended to use these ones depending on platform.
  * Win10: 3.8.7
  * Linux: 3.8.5
  * Mac osx: 3.8.8
  * Raspberry: 3.7.3

* It is recommended to create a dedicated python virtual environment and install the packages into the virtual environment:  
  * `python -m venv venv`
  * `pip install tgear-sdk`

* Depending on your installation (Linux, Raspberry, Mac users) you may need to use `python3` and `pip3` instead of `python` and `pip` respectively


##  3. <a name='Licensing'></a>Licensing

In order to perform new training and download them you need to register on following web side:
`https://www.thetactigon.com/ai/web/`
Once registration is done you can go to Profile section and click on `Json File` button to download file user_data.json
The use of this file is described later in this doc.

##  4. <a name='Tactigon Skin'></a>Tactigon Skin

###  4.1. <a name='Statusled'></a>Status led
Tactigon Skin led indicates current fucntional state:
 * when not paired to any device it rotates red/green/blue led
 * when paired (connected to PC/raspberry/smartphone) but not transmitting any data, blue led blinks
 * when paired and transmitting data, grean led blinks

##  5. <a name='T-GearSDKGeneralSetup'></a>Tactigon Gear SDK General example

When using TGear SDK the following steps are needed:

```python
# Import library
from datetime import datetime 
from tgear_sdk import TGear_Engine
from tgear_sdk.models import HAL, RealTimeConfig, Voice, TGear_Pipes_Name

# initialize config objects
hal = Hal(BLE_RIGHT_ADDRESS="MAC:ADDRESS:RIGHT:DEVICE", BLE_RIGHT_NAME="TACTI", BLE_RIGHT_ENABLE=True, 
          BLE_RIGHT_ADDRESS="", BLE_RIGHT_NAME="", BLE_RIGHT_ENABLE=False)

real_time = RealTimeConfig(MODEL_NAME_RIGHT="MODEL_R")

voice = Voice(model="path/to/model", scorer="path/to/scorer")

# initialize tgear_engine
tgear = TGear_Engine(hal, real_time, voice)

# configure tgear_engine to use right tskin and trasmit gesture, angle, button and voice data
tgear.config("RIGHT", gesture_pipe_en=True, angle_pipe_en=True, button_pipe_en=True, voice_pipe_en=True)

# get end of pipe to collect sent data
gesture = tgear.get_pipe("RIGHT", TGear_Pipes_Name.GEST)
angle = tgear.get_pipe("RIGHT", TGear_Pipes_Name.ANGLE)
button = tgear.get_pipe("RIGHT", TGear_Pipes_Name.BUTTON)
voice = tgear.get_pipe("RIGHT", TGear_Pipes_Name.VOICE)

TICK_PERIOD_MS = 100
tick = datetime.now()

g = None
a = None
b = None

# start sending
tgear.start()

while True:
  
  if gesture and gesture.poll():
    g = gesture.recv()

  if angle and angle.poll():
    a = angle.recv()

  if button and button.poll():
    b = button.recv()

  delta = datetime.now() - tick

  if delta.total_seconds() < TICK_PERIOD_MS/1000:
      continue

  tick = datetime.now()

  print("gesture:", g, "| angle:", a, "| button:", b)

  if b == [1]:
    print("stop")
    break
  elif b == [4]:
    print("voice")
    tgear.select_voice("RIGHT")

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
        , voice
        , self.tgear.voice.stop_hotword
    )

    print(tree)

    print("stop voce")
    tgear.select_sensors("RIGHT")
  g = None
  a = None
  b = None

tgear.stop()
```
##  6. <a name='T-GearSDKTrainingInstructions'></a>Tactigon Gear CLI instructions

To run the Tactigon Gear CLI open a command window (cmd/powerShell in Windows, terminal windows for all the others O.S.), move to installation folder and run the python script `cli.py` with the following command:
  * `python cli.py`

The following menu will appear:
  ```CMD
  Gear SDK Client, select an option:
  Enter 0 to test server connection
  Enter 1 to data collection
  Enter 2 to send data to server
  Enter 3 to train a new model
  Enter 4 to download a model from server
  Enter 5 to simple gesture recognition
  Type anything to EXIT
   ```

Regardless of choosen menu item, system is ready to use when showing message reportind succesfully connection to Tactigon Skin.
Succesfully connection is also confirmed by Tactigon Skin led (see next paragraph)  

Before start using the SDK user needs to change the config files according to his needs.

Linux/raspberry users: if working in SSH shell you may need to specify a DISPLAY with something like this:
  * `export DISPLAY=:0.0`
 
### 6.1. <a name='T-GearSDKConfigFiles'></a>Tactigon Gear CLI config files

Before using the SDK some general information must be set in the two following config files:

* user_data.json : Locally store login information. Need to match credentials on the server side
  ```JSON
  {
   "user_name": "joe",
   "auth_key": "_abcde123456__"
  }
  ```
* hal.json : This config file store all necessary hardware related information
  ```JSON
  {
  "BLE_RIGHT_ADDRESS": "BE:A5:7F:47:54:65", # Tactigon Right BLE Address (See Find Tactigon BLE Address section)
  "BLE_LEFT_ADDRESS": "BE:A5:7F:47:54:65",  # Tactigon Left BLE Address (See Find Tactigon BLE Address section)
  "BLE_RIGHT_ENABLE" : "True",  # Tactigon Right enable flag
  "BLE_LEFT_ENABLE" : "True",   # Tactigon Left enable flag
  "SERIAL_COM_PORT": "COM3",  # No need to change - debug 
  "NUM_SAMPLE": 10,           # No need to change - debug
  "INTERFACE" : "Bluetooth"   # No need to change - debug
  }
  ```

* client.json : This config file store http client related information
  ```JSON
  {
  "SERVER_URL": "https://tgear.eu.pythonanywhere.com", # Tactigon Gear Server IP Address
  "TRAINING_SESSIONS": ["26_02_2021_1", "26_02_2021_2"], # list of session to upload (see Training section)
  "MODEL_SESSIONS": ["26_02_2021_1", "26_02_2021_2"], # list of session for model building (see Model Building section)
  "MODEL_GESTURES": ["circle", "square"], # list of gestures recognized by the model (see Model Building section)
  "MODEL_NAME": "MODEL_RIGHT", # name assigned to the requested model (see Model Building section)
  "MODEL_DATA_PATH": "data/models/",  # No need to change
  "USER_DATA_PATH": "config_files/user_data.json",  # No need to change
  "RES": {                    # No need to change - debug 
    "user": " ",              # No need to change - debug 
    "password": " ",          # No need to change - debug  
    "status": "unsuccessful"  # No need to change - debug 
  }
  ```

### 6.2. <a name='T-GearSDKConfigFiles'></a>Tactigon Gear CLI training session

* Before running a training session the /config_files/data_collection.json data must be edited:

  * data_collection.json : This config file store all necessary information for data collection
  ```JSON
  {
  "RAW_DATA_PATH": "./data/raw/",     # path where you want to store raw data - no need to change
  "GESTURE_NAME": ["square_cw","circle_acw"],   # list of gestures you want to record
  "SESSION_INFO": "19_02_2021_A",     # recording session information
  "HAND": "RIGHT"                     # which hand is going to be used (right/left)
   }
  ```
* Turn ON the Tactigon used for the training session
* Run the `main.py` python script
* Select option 1 `Enter 1 for data collection`
* Wait for te Tactigon to be connected and activate gesture recognition by pressing button 4 on the Tactigon
* Follow console instructions to train all the gestures entered in the data_collection.json config file
* At the end of the training select option 8 `Enter 9 for EXIT` to exit the client

### 6.3. <a name='T-GearSDKTrainingDataUpload'></a>Tactigon Gear CLI Training Data Upload

Once user has run one or more training session (even with different gesture sets), training data can be uploaded to the server and used later on to generate a Model. To do that follow the instructions below:
* Edit the "TRAINING_SESSIONS" field int the`client.json` config file including all the sessions that user wants to upload to the server. Session are indicated by the "SESSION_INFO" field in the `data_collection.json` config file used during training.
* Run the `main.py` python script
* Check server connection select option 0 `Enter 0 to test server connection`
* Select option 2 `Enter 2 to send data to server`
* `Enter 9 for EXIT` to exit the client

### 6.4. <a name='T-GearSDKModelBuildingInstructions'></a>Tactigon Gear CLI Model Building Instructions

* Edit the "MODEL_SESSIONS" field int the`client.json` config file including all the sessions that user wants to use for building the model. Session are indicated by the "SESSION_INFO" field in the `data_collection.json` config file used during training.
* Edit the "MODEL_GESTURES" field int the`client.json` config file including all the gestures that the model has to recognize.
* Edit the "MODEL_NAME" field int the`client.json` config file to assign a name to the generated model.
* Run the `main.py` python script
* Check server connection select option 0 `Enter 0 to test server connection`
* Select option 3 `Enter 3 to train a new model`
* A new model is created on server side and stored to DataBase
* `Enter  for EXIT` to exit the client


### 6.5. <a name='T-GearSDKModelDownloadInstructions'></a>Tactigon Gear CLI Model Download Instructions

* Edit the "MODEL_NAME" field int the`client.json` config file to select the model to download from server.
* Select option 4 `Enter 4 to download model from server`


### 6.6. <a name='T-GearSDKGestureRecognitionSetupandTest'></a>Tactigon Gear CLI Gesture Recognition Setup and Test

* Before using the gesture recognition feature the /config_files/real_time.json data must be edited:

  - real_time.json : This config file store the models name used by the gesture recognition engine
  ```JSON
  {
  "MODEL_NAME_RIGHT": "MODEL_RIGHT",  # name of the model used for right hand gesture recognition
  "MODEL_NAME_LEFT": "MODEL_LEFT",    # name of the model used for left hand gesture recognition
  "MODEL_PATH": "data/models/" # No need to change
   }
  ```
* Run the `cli.py` python script
* Select option 5 `Enter 5 for simple gesture recognition`
* Recognized gestures will be printed on the terminal
* `Enter 9 for EXIT` to exit the client

# Appendix

The T-GEAR SDK data flow:

![](https://github.com/TactigonTeam/TGear_SDK/blob/be95a1c06ede5dd80b17e378e5df58a503144178/src/docs/img/data_flow.JPG)