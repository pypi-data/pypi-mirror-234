# PySyst - FileProperties

''' This is the "FileProperties" module. '''

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
import pathlib
import datetime
import mimetypes

# Class 1 - FileProperties
class FileProperties:
    # Function 1 - Init
    def __init__(self, path):
        # Checking the Data Type of "path"
        if (isinstance(path, str)):
            # Checking if File Path Exists
            if (os.path.exists(path)):
                # Initializing Mimetypes
                mimetypes.init()

                # Specifying and Declaring the Attributes
                self.size = os.path.getsize(path)

                self.file_name = os.path.basename(path).split("/")[-1]
                self.file_type = mimetypes.guess_type(path)[0].split("/")[0]
                self.file_extension = pathlib.Path(path).suffix

                self.creation = str(datetime.datetime.fromtimestamp(os.path.getctime(path)))
                self.creation_datetime = datetime.datetime.fromtimestamp(os.path.getctime(path))
                self.modification = str(datetime.datetime.fromtimestamp(os.path.getmtime(path)))
                self.modification_datetime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
                self.accessed = str(datetime.datetime.fromtimestamp(os.path.getatime(path)))
                self.accessed_datetime = datetime.datetime.fromtimestamp(os.path.getatime(path))

                self.absolute_path = os.path.abspath(path)
                self.directory_path = os.path.dirname(path)
            else:
                raise FileNotFoundError("The file path doesn't exist.")
        else:
            raise TypeError("The 'path' argument must be a string.")