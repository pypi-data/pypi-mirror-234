import os
import sys
import json
from .frog_params import Params

class UtilityDetails:

    def __init__(self) -> None:
        self.description = "This utility has not been given a description"
        self.params = Params()

        # Currently applicable to system utilities only
        self.category =""

    def to_json(self) -> str:

        # Name is taken automatically from the name of the utility script being run
        name = os.path.splitext(os.path.basename(sys.modules['__main__'].__file__))[0]

        dict = {"Name": name,
                "Category": self.category,
                "Description": self.description,
                "Params": self.params.result()}
        
        return json.dumps(dict)