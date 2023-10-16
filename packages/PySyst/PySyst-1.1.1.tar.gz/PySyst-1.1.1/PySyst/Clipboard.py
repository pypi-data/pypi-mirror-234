# PySyst - Clipboard

''' This is the "Clipboard" module. '''

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
import pyperclip

# Function 1 - Copy
def copy(data):
    # Checking the Data Type of "data"
    if (isinstance(data, (str, int, float, bool))):
        # Copying the Data
        pyperclip.copy(data)
    else:
        raise TypeError("The 'data' argument must be a string, integer, float, or a boolean.")

# Function 2 - Copy File
def copy_file(path):
    # Checking the Data Type of "path"
    if (isinstance(path, str)):
        # Checking if Path Exists
        if (os.path.exists(path)):
            # Opening the File
            try:
                with open(path) as file:
                    # Copying the File
                    copy(file.read())
            except:
                raise Exception("An error occurred while copying the contents of the file. Please try again.")
        else:
            raise FileNotFoundError("The file path doesn't exist.")
    else:
        raise TypeError("The 'path' argument must be a string.")

# Function 3 - Paste
def paste():
    # Returning the Last Copied Item
    return pyperclip.paste()

# Function 4 - Paste File
def paste_file(path):
    # Checking the Data Type of "path"
    if (isinstance(path, str)):
        # Opening the File
        try:
            with open(path, "w") as file:
                # Pasting the Data to the File
                file.write(paste())
        except:
            raise Exception("An error occurred while pasting the data to the file. Please try again.")
    else:
        raise TypeError("The 'path' argument must be a string.")