from .Challenge import Challenge
from pwn import *

class BackToBasic(Challenge):
    flag_location = 'flags/back-to-basic.txt'
    history_location = 'history/back-to-basic.txt'

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
            r = remote("localhost",self.port)
            assert b"idea?" in r.recvline(), "Failed First"

            r.sendline(b"testt")

            assert b"thing" in r.recvline(), "Failed Last"

            return True
        except Exception as e:
            self.logger.error(f'Could not check back-to-basic: {e}')
            return False
