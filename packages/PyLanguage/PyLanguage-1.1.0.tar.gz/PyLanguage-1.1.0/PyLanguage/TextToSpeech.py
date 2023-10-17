# PyLanguage - TextToSpeech

''' This is the "TextToSpeech" module. '''

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
import pyttsx3
from types import NoneType

# Function 1 - Get Property
def get_property(property, driver=None, debug=False):
    # Variables
    properties = ["rate", "voice", "voices", "volume", "pitch"]
    drivers = ["sapi5", "nsss", "espeak"]
    parameters = ["property", "driver", "debug"]

    # Parameters & Data Types
    paramaters_data = {
        "property": [str, "a string"],
        "driver": [(str, NoneType), "a string"],
        "debug": [bool, "a boolean"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Checking the Value of "driver" and Creating the Engine
    if (driver == None):
        engine = pyttsx3.init(debug=debug)
    elif (driver in drivers):
        engine = pyttsx3.init(driverName=driver, debug=debug)
    else:
        raise Exception("The 'driver' argument must be a valid driver's name. The available drivers are:\n\n" + str(drivers))

    # Checking the Value of "property"
    if (property in properties):
        # Try/Except
        try:
            # Fetching the Property
            fetchedProperty = engine.getProperty(property)

            # Stopping the Engine
            engine.stop()

            # Returning the Property
            return fetchedProperty
        except:
            raise Exception("Failed to fetch the '{0}' property.".format(property))
    else:
        raise Exception("The 'property' argument must be a valid property's name. The available properties are:\n\n" + str(properties))

# Function 2 - Say
def say(text, rate=200, voice=get_property("voices")[0].id, volume=1.0, pitch=0.5, onStart=None, onWordStart=None, onWordEnd=None, onEnd=None, onError=None, driver=None, debug=False):
    # Variables
    drivers = ["sapi5", "nsss", "espeak"]
    parameters = ["text", "rate", "voice", "volume", "pitch", "driver", "debug"]

    # Parameters & Data Types
    paramaters_data = {
        "text": [str, "a string"],
        "rate": [int, "an integer"],
        "voice": [str, "a string"],
        "volume": [float, "a float"],
        "pitch": [float, "a float"],
        "driver": [(str, NoneType), "a string"],
        "debug": [bool, "a boolean"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Checking the Value of "driver" and Creating the Engine
    if (driver == None):
        engine = pyttsx3.init(debug=debug)
    elif (driver in drivers):
        engine = pyttsx3.init(driverName=driver, debug=debug)
    else:
        raise Exception("The 'driver' argument must be a valid driver's name. The available drivers are:\n\n" + str(drivers))

    # Try/Except - Converting Text to Speech
    try:
        # Setting the Events
        if ((onStart != None) and (callable(onStart))):
            engine.connect("started-utterance", onStart)

        if ((onWordStart != None) and (callable(onWordStart))):
            engine.connect("started-word", onWordStart)

        if ((onWordEnd != None) and (callable(onWordEnd))):
            engine.connect("finished-word", onWordEnd)

        if ((onEnd != None) and (callable(onEnd))):
            engine.connect("finished-utterance", onEnd)

        if ((onError != None) and (callable(onError))):
            engine.connect("error", onError)

        # Setting the Properties
        engine.setProperty("rate", rate)
        engine.setProperty("voice", voice)
        engine.setProperty("volume", volume)
        engine.setProperty("pitch", pitch)

        # Converting Text to Speech
        engine.say(text)
        engine.runAndWait()
    except:
        raise Exception("An error occurred while converting the text to speech. Please try again.")

# Function 3 - Save
def save(text, path, rate=200, voice=get_property("voices")[0].id, volume=1.0, pitch=0.5, onStart=None, onWordStart=None, onWordEnd=None, onEnd=None, onError=None, driver=None, debug=False):
    # Variables
    drivers = ["sapi5", "nsss", "espeak"]
    parameters = ["text", "path", "rate", "voice", "volume", "pitch", "driver", "debug"]

    # Parameters & Data Types
    paramaters_data = {
        "text": [str, "a string"],
        "path": [str, "a string"],
        "rate": [int, "an integer"],
        "voice": [str, "a string"],
        "volume": [float, "a float"],
        "pitch": [float, "a float"],
        "driver": [(str, NoneType), "a string"],
        "debug": [bool, "a boolean"]
    }

    # Checking the Data Types
    for parameter in parameters:
        if (isinstance(eval(parameter), paramaters_data[parameter][0])):
            pass
        else:
            raise TypeError("The '{0}' argument must be {1}.".format(parameter, paramaters_data[parameter][1]))

    # Checking the Value of "driver" and Creating the Engine
    if (driver == None):
        engine = pyttsx3.init(debug=debug)
    elif (driver in drivers):
        engine = pyttsx3.init(driverName=driver, debug=debug)
    else:
        raise Exception("The 'driver' argument must be a valid driver's name. The available drivers are:\n\n" + str(drivers))

    # Try/Except - Saving the File
    try:
        # Setting the Events
        if ((onStart != None) and (callable(onStart))):
            engine.connect("started-utterance", onStart)

        if ((onWordStart != None) and (callable(onWordStart))):
            engine.connect("started-word", onWordStart)

        if ((onWordEnd != None) and (callable(onWordEnd))):
            engine.connect("finished-word", onWordEnd)

        if ((onEnd != None) and (callable(onEnd))):
            engine.connect("finished-utterance", onEnd)

        if ((onError != None) and (callable(onError))):
            engine.connect("error", onError)

        # Setting the Properties
        engine.setProperty("rate", rate)
        engine.setProperty("voice", voice)
        engine.setProperty("volume", volume)
        engine.setProperty("pitch", pitch)

        # Saving the File
        engine.save_to_file(text, path)
        engine.runAndWait()
    except:
        raise Exception("An error occurred while saving the file. Please try again.")