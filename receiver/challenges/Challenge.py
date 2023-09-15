import logging
import random
import string

from config import get_settings


class Challenge(object):
    name = __name__
    settings = get_settings()
    port = 0

    def __init__(self, port):    
        self.port = port
        self.add_logger()

    def add_logger(self):
        self.logger = logging.getLogger()

    def random_string(self, length):
        charset = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choice(charset) for i in range(length))

    def distribute(self, flag):
        raise NotImplementedError

    def check(self):
        raise NotImplementedError

    def credentials(self):
        return {
            'username': 'root',
            'password': getattr(self.settings, f'PASSWORD_{self.port}'),
        }
