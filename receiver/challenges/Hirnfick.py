import requests
from base64 import b64decode

from .Challenge import Challenge


class Hirnfick(Challenge):
    flag_location = 'flags/hirnfick.txt'
    history_location = 'history/hirnfick.txt'

    def distribute(self, flag):
        try:
            with open(self.flag_location, 'w') as f:
                f.write(flag)

            with open(self.history_location, 'a') as f:
                f.write(flag + '\n')

            self.logger.info(f'Flag {flag} written to {self.flag_location}')
            return True

        except Exception as e:
            self.logger.error(
                f'Could not write flag to {self.flag_location}: {e}')
            return False

    def check(self):
        try:
            res = requests.post(
                f"http://localhost:{self.port}/api/run",
                timeout=5,
                json={
                    "code":
                    "+[-->-[>>+>-----<<]<--<---]>-.>>>+.>>..+++[.>]<<<<.+++.------.<<-.>>>>+."
                })

            assert b64decode(res.json()["output"]) == b"HirnFick 1.0\nHello, World!"

            return True
        except Exception as e:
            self.logger.error(f'Could not check hirnfick: {e}')
            return False
