from .Challenge import Challenge

import requests
import os


class S3(Challenge):
    flag_location = 'flags/s3.txt'
    history_location = 'history/s3.txt'
    host = 'http://localhost:20000'

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
            filename = self.random_string(8) + ".txt"
            content = self.random_string(64)

            r = requests.post(f"http://localhost:{self.port}/upload", files={'file': (filename, content)})
            assert r.status_code == 200
            assert r.text == f'Download <a href="/download?filename={filename}">here</a>'

            r = requests.get(f"http://localhost:{self.port}/download?filename={filename}")
            assert r.status_code == 200
            assert r.text == content

            return True

        except Exception as e:
            self.logger.error(f'Could not check s3: {e}')
            return False
