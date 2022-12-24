import pandas as pd
import numpy as np
from fastapi import UploadFile, File


# A class which will convert the upload curriculum to JSON response
# to foster ease of processing in javascript
class CurriculumWrangler:

    # Constructor which initializes the path to the temporarily
    # stored curriculum.
    def __init__(self, file: UploadFile = File(...)):
        self.FILE = file.file
        self.curriculum = None
        self.response = dict()

    # Function which loads the temporarily stored curriculum and
    # converting it into a dictionary.
    def load_curriculum(self):
        try:
            #print(self.FILE.read())
            self.curriculum = pd.read_csv(self.FILE)
            self.curriculum = self.curriculum.to_dict()
        except pd.errors.ParserError:
            self.response = {
                "IsError" : True,
                "Error" : "FileTypeMismatch",
                "Message" : "Pandas can only accept tabular data."
            } 

    # Function which transforms the curriculum into a API response
    # which relevant data if formatting requirements are met.
    def transform_curriculum(self):
        if self.curriculum == None:
            return self.response

        try:
            for i in self.curriculum["Course Code"]:
                key = self.curriculum["Course Code"][i]
                self.response[key] = dict()
                course_duration = self.curriculum["Duration"][i]
                if type(course_duration) != type(3.45):
                    course_duration = (
                        course_duration.replace("weeks", "").strip().split("-")
                    )
                    if "-" in course_duration:
                        self.response[key]["Duration"] = int(
                            np.mean(list(map(int, course_duration)))
                        )
                    else:
                        self.response[key]["Duration"] = int(course_duration[0])
                else:
                    self.response[key]["Duration"] = 30

                if type(self.curriculum["Prerequisite Codes"][i]) != type(3.45):
                    self.response[key]["Prerequisite Codes"] = self.curriculum[
                        "Prerequisite Codes"
                    ][i].split(";")
                else:
                    self.response[key]["Prerequisite Codes"] = []
            
            self.response = {
                "IsError": False,
                "Curriculum":self.response
            }

        except KeyError as k:
            print(self.response)

            self.response = {
                "IsError" : True,
                "Error": "CurriculumSchemaMismatchError",
                "Message": "The curriculum schema does not follow the formatting requirements",
            }

        return self.response
