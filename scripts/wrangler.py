import pandas as pd
import numpy as np


# A class which will convert the upload curriculum to JSON response
# to foster ease of processing in javascript
class CurriculumWrangler:
    
    # Constructor which initializes the path to the temporarily 
    # storaged curriculum.
    def __init__(self, path : str):
       self.PATH = path
       self.curriculum = None
       self.response = dict()
    
    # Function which loads the temporarily stored curriculum and 
    # converting it into a dictionary.
    def load_curriculum(self):
       self.curriculum = pd.read_csv(self.PATH)
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
                  course_duration = course_duration.replace("weeks","").split("-").strip()
                  if "-" in course_duration:
                     self.response[key]["Duration"] = int(np.mean(list(map(int, 
                                                                           course_duration))))
                  else:
                     self.response[key]["Duration"] = int(course_duration)
               else:
                  self.response[key]["Duration"] = 30
               self.response[key]["Prerequisites"] = self.curriculum["Prerequisites"].split(";")
       except KeyError:
            self.response = { "Error": "CurriculumSchemaMismatchError", 
                              "CurriculumSchemaMismatchError": "The curriculum schema does not follow the formatting requirements"}
    
       

    
