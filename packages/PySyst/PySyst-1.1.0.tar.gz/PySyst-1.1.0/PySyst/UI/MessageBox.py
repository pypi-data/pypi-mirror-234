# PySyst (UI) - MessageBox

''' This is the "MessageBox" module. '''

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
import os
#import platform
import pyautogui
from types import NoneType
#from win10toast import ToastNotifier

# Function 1 - Alert
def alert(title="", text="", button=""):
    # Variables
    parameters = ["title", "text", "button"]

    # Parameters & Data Types
    paramaters_data = {
        "title": [str, "a string"],
        "text": [str, "a string"],
        "button": [str, "a string"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Displaying the Message Box
    pyautogui.alert(title=title, text=text, button=button)

# Function 2 - Confirm
def confirm(title="", text="", buttons=[]):
    # Variables
    parameters = ["title", "text", "buttons"]

    # Parameters & Data Types
    paramaters_data = {
        "title": [str, "a string"],
        "text": [str, "a string"],
        "buttons": [list, "a list"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Displaying the Message Box
    pyautogui.confirm(title=title, text=text, buttons=buttons)

# Function 3 - Prompt
def prompt(title="", text="", default=""):
    # Variables
    parameters = ["title", "text", "default"]

    # Parameters & Data Types
    paramaters_data = {
        "title": [str, "a string"],
        "text": [str, "a string"],
        "default": [str, "a string"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Displaying the Message Box
    return pyautogui.prompt(title=title, text=text, default=default)

# Function 4 - Password
def password(title="", text="", default="", mask="*"):
    # Variables
    parameters = ["title", "text", "default", "mask"]

    # Parameters & Data Types
    paramaters_data = {
        "title": [str, "a string"],
        "text": [str, "a string"],
        "default": [str, "a string"],
        "mask": [str, "a string"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Displaying the Message Box
    return pyautogui.password(title=title, text=text, default=default, mask=mask)

# Function 5 - Toast
'''def toast(title, message, icon=None, duration=5, threaded=False):
    # Variables
    parameters = ["title", "message", "icon", "duration", "threaded"]

    # Parameters & Data Types
    paramaters_data = {
        "title": [str, "a string"],
        "message": [str, "a string"],
        "icon": [(str, NoneType), "a string"],
        "duration": [(int, float), "an integer or a float"],
        "threaded": [bool, "a boolean"]
    }

    # Checking the OS
    if (platform.uname().system == "Windows"):
        pass
    else:
        raise Exception("This function only works on Windows.")

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Checking if "icon" Path Exists
    if (icon != None):
        if (os.path.exists(icon)):
            raise FileNotFoundError("The 'icon' file path doesn't exist.")

    # Displaying the Toast
    ToastNotifier().show_toast(title, message, icon_path=icon, duration=duration, threaded=threaded)'''