import pandas as pd
import numpy as np
from fastapi import UploadFile, File


# A class which will convert the upload curriculum to JSON response
# to foster ease of processing in javascript
class CurriculumWrangler:

    # Constructor which initializes the path to the temporarily
    # storaged curriculum.
    def __init__(self, file: UploadFile = File(...)):
        self.FILE = file.file
        self.curriculum = None
        self.response = dict()

    # Function which loads the temporarily stored curriculum and
    # converting it into a dictionary.
    def load_curriculum(self):
        self.curriculum = pd.read_csv(self.FILE)
        self.curriculum = self.curriculum.to_dict()

    # Function which transforms the curriculum into a API response
    # which relevant data if formatting requirements are met.
    def transform_curriculum(self):
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
        except KeyError as k:
            print(self.response)

            self.response = {
                "Error": "CurriculumSchemaMismatchError",
                "CurriculumSchemaMismatchError": "The curriculum schema does not follow the formatting requirements",
            }

        return self.response
