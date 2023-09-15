from .Challenge import Challenge

import requests


class Pasta(Challenge):
    flag_location = 'flags/pasta.txt'
    history_location = 'history/pasta.txt'
    host = "http://localhost:13000"

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
            username = f"checker-{self.random_string(8)}"
            pwd = self.random_string(12)
            flag = open(self.flag_location).read()

            admin_data = {
                'username': 'deomkicer_number_1_fans',
                'password': getattr(self.settings, f'PASSWORD_{self.port}'),
            }

            # login admin and check flag
            response = requests.post(
                f"{url}/auth",
                json=admin_data).json()

            token = response.get('token')
            assert token, "Token is missing in login admin"
            check_flag = requests.get(f"{url}/flag", headers={'Authorization': f"Bearer {token}"}).json()
            assert check_flag.get('flag') == flag, "Flag is missing/mismatch"

            # register
            response = requests.post(
                f"{url}/register",
                json={
                    "username": f"{username}",
                    "password": f"{pwd}"}).json()

            assert response.get('success') == "User registered succesfully", "Register failed"

            # login with version 1
            response = requests.post(
                f"{url}/auth?version=1",
                json={
                    "username": f"{username}",
                    "password": f"{pwd}"}).json()

            token = response.get('token')
            assert token, "Token is missing in login v1"
            check_home = requests.get(f"{url}/", headers={'Authorization': f"Bearer {token}"}).json()
            assert check_home.get('username') == username, "Different username found in login v1"

            # login with version 2
            response = requests.post(
                f"{url}/auth?version=2",
                json={
                    "username": f"{username}",
                    "password": f"{pwd}"}).json()

            token = response.get('token')
            assert token, "Token is missing in login v2"
            check_home = requests.get(f"{url}/", headers={'Authorization': f"Bearer {token}"}).json()
            assert check_home.get('username') == username, "Different username found in login v2"

            # login with version 3
            response = requests.post(
                f"{url}/auth?version=3",
                json={
                    "username": f"{username}",
                    "password": f"{pwd}"}).json()

            token = response.get('token')
            assert token, "Token is missing in login v3"
            check_home = requests.get(f"{url}/", headers={'Authorization': f"Bearer {token}"}).json()
            assert check_home.get('username') == username, "Different username found in login v3"

            # login with version 4
            response = requests.post(
                f"{url}/auth?version=4",
                json={
                    "username": f"{username}",
                    "password": f"{pwd}"}).json()

            token = response.get('token')
            assert token, "Token is missing in login v4"
            check_home = requests.get(f"{url}/", headers={'Authorization': f"Bearer {token}"}).json()
            assert check_home.get('username') == username, "Different username found in login v4"

            return True

        except Exception as e:
            self.logger.error(f'Could not check pasta: {e}')
            return False
