from .Challenge import Challenge

import io
import pandas as pd
import requests
import re

MOCK_DATA = [
    {'name': 'John','age': 30, 'city': 'New York'},
    {'name': 'Mary', 'age': 25, 'city': 'San Francisco'},
    {'name': 'Peter', 'age': 45, 'city': 'Chicago'},
]

MOCK_RESULT = {
    "Sheet1":{
        "!ref":"A1:C4",
        "A1":{"t":"s","v":"name","h":"name","w":"name"},"B1":{"t":"s","v":"age","h":"age","w":"age"},"C1":{"t":"s","v":"city","h":"city","w":"city"},
        "A2":{"t":"s","v":"John","h":"John","w":"John"},"B2":{"t":"n","v":30,"w":"30"},"C2":{"t":"s","v":"New York","h":"New York","w":"New York"},
        "A3":{"t":"s","v":"Mary","h":"Mary","w":"Mary"},"B3":{"t":"n","v":25,"w":"25"},"C3":{"t":"s","v":"San Francisco","h":"San Francisco","w":"San Francisco"},
        "A4":{"t":"s","v":"Peter","h":"Peter","w":"Peter"},"B4":{"t":"n","v":45,"w":"45"},"C4":{"t":"s","v":"Chicago","h":"Chicago","w":"Chicago"},
        "!margins":{"left":0.75,"right":0.75,"top":1,"bottom":1,"header":0.5,"footer":0.5}
        }
    }

class XL(Challenge):
    flag_location = 'flags/xl.txt'
    history_location = 'history/xl.txt'
    

    def distribute(self, flag):
        try:
            with open(self.flag_location, 'w') as f:
                f.write(flag)
            
            with open(self.history_location, 'a') as f:
                f.write(flag + '\n')

            self.logger.info(f'Flag {flag} written to {self.flag_location}')
            return True

        except Exception as e:
            self.logger.error(f'Could not write flag to {self.flag_location}: {e}')
            return False

    def check(self):
        try:
            url = f'http://localhost:{self.port}'
            files = {'file': self.generate_mock_file()}
            r = requests.post(url, files=files, timeout=5)
            assert r.json() == MOCK_RESULT, 'Unexpected response'
            self.logger.info('Check passed for xl')
            
            return True

        except Exception as e:
            self.logger.error(f'Could not check xl: {e}')
            return False

    def generate_mock_file(self):
        memory_file = io.BytesIO()
        
        df = pd.DataFrame(MOCK_DATA)
        df.to_excel(memory_file, index=False)
        
        memory_file.seek(0)
        return memory_file
