from .Challenge import Challenge

import requests
import os

MOCK_URL = 'http://google.com'
MOCK_DATA = '<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">'

class Crawlback(Challenge):
    flag_location = 'flags/crawlback.txt'
    history_location = 'history/crawlback.txt'

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
            r = requests.post(f"http://localhost:{self.port}/crawlback.php", data={'url': MOCK_URL})

            assert r.text.split('\n').pop(0) == MOCK_DATA

            return True

        except Exception as e:
            self.logger.error(f'Could not check crawlback: {e}')
            return False
