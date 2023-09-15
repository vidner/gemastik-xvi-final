from .Challenge import Challenge

from fastecdsa.curve import Curve
from fastecdsa.point import Point
import requests
import time
import os
import json


class Burvesigner(Challenge):
    flag_location = 'flags/burvesigner.txt'
    history_location = 'history/burvesigner.txt'
    priv_location = 'files/burvesigner.priv'

    def distribute(self, flag):
        try:
            with open(self.flag_location, 'w') as f:
                f.write(flag)

            with open(self.priv_location, 'wb') as f:
                f.write(os.urandom(256))

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
            flag = open(self.flag_location).read()

            # C1: login guest success
            guest_data = {
                'username': 'guest',
                'password': 'guest',
            }
            response = requests.post(url, data=guest_data, timeout=5)
            guest_token = response.cookies["token"]
            assert "Welcome, guest!" in response.text, "Guest cannot login"
            assert "flashes" not in response.text, "Guest cannot login"
            self.logger.info(f'C1 success for burvesigner')

            # C2: login admin success
            admin_data = {
                'username': 'merricx_number_1_fans',
                'password': getattr(self.settings, f'PASSWORD_{self.port}'),
            }
            response = requests.post(url, data=admin_data, timeout=5)
            admin_token = response.cookies["token"]
            assert "Welcome, merricx_number_1_fans!" in response.text, "Admin cannot login"
            assert flag in response.text, "Flag is missing in admin page"
            assert "flashes" not in response.text, "Admin cannot login"
            self.logger.info(f'C2 success for burvesigner')

            # C3: login guest fail
            guest_data = {
                'username': 'guest',
                'password': 'Guest',
            }
            response = requests.post(url, data=guest_data, timeout=5).text
            assert "Welcome, guest!" not in response, "Guest with wrong credential can login"
            assert "flashes" in response, "Guest with wrong credential can login"
            self.logger.info(f'C3 success for burvesigner')

            # C4: login admin fail
            admin_data = {
                'username': 'merricx_number_1_fans',
                'password': 'password',
            }
            response = requests.post(url, data=admin_data, timeout=5).text
            assert "Welcome, merricx_number_1_fans!" not in response, "Admin with wrong credential can login"
            assert flag not in response, "Flag is showing in admin page with wrong credential"
            assert "flashes" in response, "Admin with wrong credential can login"
            self.logger.info(f'C4 success for burvesigner')

            self.logger.info('calling sleep(5)')
            time.sleep(5)

            # C5: cek apakah token guest di C1 sudah expired atau belum
            response = requests.get(url, cookies={"token": guest_token}, timeout=5)
            assert "Welcome, guest!" in response.text, "Guest token expires early"
            assert "flashes" not in response.text, "Guest token expires early"
            self.logger.info(f'C5 success for burvesigner')

            # C6: cek apakah token admin di C2 sudah expired atau belum
            response = requests.get(url, cookies={"token": admin_token}, timeout=5)
            assert "Welcome, merricx_number_1_fans!" in response.text, "Admin token expires early"
            assert flag in response.text, "Admin token expires early"
            assert "flashes" not in response.text, "Admin token expires early"
            self.logger.info(f'C6 success for burvesigner')

            # C7: cek endpoint /params
            response = requests.get(url + "/params", timeout=5).text
            response = response.replace("<pre>", "").replace("</pre>", "")
            params = json.loads(response)
            assert params["p"] and params["a"] and params["b"] and params["n"], "Missing p, a, b and/or n parameter(s)"
            assert params["G"][0] and params["G"][1] and params["Y"][0] and params["Y"][1], "Missing G and/or Y point(s)"
            self.logger.info(f'C7 success for burvesigner')

            # C8: cek apakah curve C valid dan point G di C
            C = Curve("burvesigner", params["p"], params["a"], params["b"], params["n"], params["G"][0], params["G"][1])
            assert C.G == Point(params["G"][0], params["G"][1], C), "Point G is not valid"
            self.logger.info(f'C8 success for burvesigner')

            # C9: cek apakah point G * priv = Y
            t = params["p"].bit_length() // 8
            priv = open(self.priv_location, "rb").read()[:t]
            x = int.from_bytes(priv, "little")
            Y = Point(params["Y"][0], params["Y"][1], C)
            assert C.G * x == Y, "Point Y is not valid"
            self.logger.info(f'C9 success for burvesigner')

            return True

        except Exception as e:
            self.logger.error(f'Could not check burvesigner: {e}')
            return False
