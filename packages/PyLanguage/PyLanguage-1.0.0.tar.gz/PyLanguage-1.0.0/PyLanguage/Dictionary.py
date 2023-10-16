# PyLanguage - Dictionary

''' This is the "Dictionary" module. '''

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
import json
import requests

# Class 1 - Dictionary
class Dictionary:
    # Function 1 - Init
    def __init__(self, word):
        # Checking the Data Type of "word"
        if (isinstance(word, str)):
            # Fetching the Data
            try:
                response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + word)
            except requests.ConnectionError:
                raise ConnectionError("A connection error occurred. Please try again.")
            except:
                raise Exception("Something went wrong. Please try again.")

            # Try/Except
            try:
                # Converting the Data to a Dictionary
                data = json.loads(response.text)[0]

                # Gathering the Meanings into a List
                meanings = []

                for meaning in data["meanings"]:
                    # Variables
                    meaningDict = {}
                    definitionsList = []

                    # Adding "part_of_speech" to "meaningDict"
                    meaningDict["part_of_speech"] = meaning["partOfSpeech"]

                    # Searching for Meanings
                    for sub_meaning in meaning["definitions"]:
                        definitionsList.append(sub_meaning["definition"])

                    # Adding "definition" to "meaningDict"
                    meaningDict["definitions"] = definitionsList

                    # Appending "meaningDict" to "meanings"
                    meanings.append(meaningDict)

                # Specifying and Declaring the Attributes
                self.word = data["word"]
                self.phonetics = data["phonetics"]
                self.meanings = meanings
                self.license = data["license"]
                self.source_urls = data["sourceUrls"]
            except:
                # Converting the Data to a Dictionary and Extracting the Title
                title = json.loads(response.text)["title"]

                # Raising Exceptions
                if (title == "No Definitions Found"):
                    raise Exception("No definitions were found for this word. Please try again.")
                elif (title == "API Rate Limit Exceeded"):
                    raise Exception("You have exceeded the rate limit. Please try again later.")
                elif (title == "Something Went Wrong"):
                    raise Exception("Something went wrong. Please try again later.")
                elif (title == "Upstream Server Failed"):
                    raise Exception("Something went wrong. Please try again later.")
        else:
            raise TypeError("The 'word' argument must be a string.")