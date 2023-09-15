from .Challenge import Challenge

import requests
import zlib
import gzip
import json

MOCK_URL = 'http://google.com'
MOCK_DATA_WGET = 'Google</title>'
MOCK_DATA_CURL = '<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">'

class GemasFetcher(Challenge):
    flag_location = 'flags/gemas-fetcher.txt'
    history_location = 'history/gemas-fetcher.txt'

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
            sess = requests.Session()

            ## register
            username = self.random_string(5)
            password = self.random_string(5)
            r = sess.post(f"http://localhost:{self.port}/auth/register", data={"username":username,"password": password}, allow_redirects=False)
            assert r.headers.get("location") == "/auth/login", "Register Failed"

            ## login
            r = sess.post(f"http://localhost:{self.port}/auth/login", data={"username":username,"password": password}, allow_redirects=False)
            assert r.headers.get("location") == "/dashboard", "Login Failed"

            ## wget
            content = {"provider": "wget","url":MOCK_URL}
            files = {"file": ("visit", b"\x00\x00"+gzip.compress(zlib.compress(json.dumps(content).encode())))}
            r = sess.post(f"http://localhost:{self.port}/dashboard/fetch_by_file", files=files)
            assert MOCK_DATA_WGET in r.text, "wget Failed"
            
            ## curl
            content = {"provider": "curl","url":MOCK_URL}
            files = {"file": ("visit", b"\x00\x01"+gzip.compress(zlib.compress(json.dumps(content).encode())))}
            r = sess.post(f"http://localhost:{self.port}/dashboard/fetch_by_file", files=files)
            assert r.text.split('\n').pop(0) == MOCK_DATA_CURL, "curl Failed"

            ## python
            content = {"provider": "python","url":MOCK_URL}
            files = {"file": ("visit", b"\x00\x02"+gzip.compress(zlib.compress(json.dumps(content).encode())))}
            r = sess.post(f"http://localhost:{self.port}/dashboard/fetch_by_file", files=files)
            assert r.text.startswith('"PCFkb2N0eXBlIGh0bWw'), "python Failed"

            return True

        except Exception as e:
            self.logger.error(f'Could not check gemas-fetcher: {e}')
            return False
