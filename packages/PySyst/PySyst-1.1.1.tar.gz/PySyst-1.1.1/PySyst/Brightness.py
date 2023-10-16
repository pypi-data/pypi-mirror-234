# PySyst - Brightness

''' This is the "Brightness" module. '''

'''
Copyright 2023 Aniketh Chavare

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

# Imports
import platform
from types import NoneType

if (platform.system() in ["Windows", "Linux"]):
    try:
        import screen_brightness_control as sbc
    except:
        raise Exception("The 'screen-brightness-control' package must be installed for this module to work.")

# Function 1 - Max
def max():
    # Checking the OS
    if (platform.system() in ["Windows", "Linux"]):
        # Setting the Brightness
        sbc.set_brightness(100)
    else:
        raise Exception("This function only works on Windows and Linux.")

# Function 2 - Min
def min():
    # Checking the OS
    if (platform.system() in ["Windows", "Linux"]):
        # Setting the Brightness
        sbc.set_brightness(0)
    else:
        raise Exception("This function only works on Windows and Linux.")

# Function 3 - Set
def set(value, display=0):
    # Variables
    parameters = ["value", "display"]

    # Parameters & Data Types
    paramaters_data = {
        "value": [(int, float), "an integer or a float"],
        "display": [(int, str), "an integer or a string"]
    }

    # Checking the OS
    if (platform.system() in ["Windows", "Linux"]):
        pass
    else:
        raise Exception("This function only works on Windows and Linux.")

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Setting the Brightness
    sbc.set_brightness(value, display=display)

# Function 4 - Fade
def fade(final, start=None, interval=0.01, increment=1, blocking=True):
    # Variables
    parameters = ["final", "start", "interval", "increment", "blocking"]

    # Parameters & Data Types
    paramaters_data = {
        "final": [(int, float), "an integer or a float"],
        "start": [(int, float, NoneType), "an integer or a float"],
        "interval": [(int, float), "an integer or a float"],
        "increment": [(int, float), "an integer or a float"],
        "blocking": [bool, "a boolean"]
    }

    # Checking the OS
    if (platform.system() in ["Windows", "Linux"]):
        pass
    else:
        raise Exception("This function only works on Windows and Linux.")

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Setting the Brightness
    sbc.fade_brightness(final, start=start, interval=interval, increment=increment, blocking=blocking)

# Function 5 - Get
def get():
    # Checking the OS
    if (platform.system() in ["Windows", "Linux"]):
        # Returning the Data
        return {"Brightness": sbc.get_brightness(), "Monitors": sbc.list_monitors_info()}
    else:
        raise Exception("This function only works on Windows and Linux.")