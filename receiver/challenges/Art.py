from .Challenge import Challenge

import io
import pandas as pd
import requests
import re

class Art(Challenge):
    flag_location = 'flags/art.txt'
    history_location = 'history/art.txt'
    

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
            word = self.random_string(8)
            url = f'http://localhost:{self.port}/art/{word}'
            r = requests.get(url, timeout=5)
            assert r.text == f'<iframe height="100%" width="100%" frameborder="0" src=https://asciified.thelicato.io/api/v2/ascii?text={word}></iframe>', 'Unexpected response'
            self.logger.info('Check passed for art')
            
            return True

        except Exception as e:
            self.logger.error(f'Could not check art: {e}')
            return False