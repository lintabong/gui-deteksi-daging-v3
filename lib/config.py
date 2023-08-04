import os
import json

class Config():
    def __init__(self):
        self.filename = "config.json"
        self.width    = 1230

        if not os.path.exists(self.filename):
            result = {
                "width": self.width,
                "height": 800,
                "titleFrame": {
                    "width": self.width,
                    "height": 60,
                    "background": "#50cc77"
                },
                "loadImageFrame": {
                    "width": self.width,
                    "height": 740,
                    "background": "#50cc77"
                },
                "executeFrame": {
                    "width": self.width,
                    "height": 200,
                    "background": "#50cc77"
                },
                "historyFrame": {
                    "width": self.width,
                    "height": 200,
                    "background": "#50cc77"
                },
                "user" : {
                    "pathfile": None
                }
            }
                    
            with open(self.filename, "w") as outfile:
                json.dump(result, outfile)
                
            outfile.close()


    def read(self):
        with open(self.filename, "r") as openfile:
            config = json.load(openfile)

        openfile.close()

        return config

    def write(self, configuration):
        with open(self.filename, "w") as outfile:
            json.dump(configuration, outfile)
            
        outfile.close()

        return 1