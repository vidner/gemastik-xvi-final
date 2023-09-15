from .Challenge import Challenge

import requests

class GemasNotes(Challenge):
    history_location = 'history/gemas-notes.txt'
    host = "http://localhost:12000"

    def distribute(self, flag):
        try:
            username = "gemasflagreceiver"
            password = "AuTeEbn%.Q5$pC_ge6"
            result = requests.post(f"{self.host}/flag_receiver", json={"flag": flag}, auth=(username,password)).json()
            if not result.get("success"):
                return False
            
            with open(self.history_location, 'a') as f:
                f.write(flag + '\n')

            self.logger.info(f'Flag {flag} updated in gemas-notes database')
            return True

        except Exception as e:
            self.logger.error(f'Could send flag to gemas-notes challenge: {e}')
            return False

    def check(self):
        try:
            url = f'http://localhost:{self.port}'
            
            # login
            token = requests.post(f"{url}/api/login",json={"email":"checker@gemasnotes.id", "password":"uRIqCvJ<IGb;VDT14"}).json()["token"]
            header = {"Authorization": f"Bearer {token}"}
            
            # get count
            old_count = requests.post(f"{url}/api/notes/count", headers=header, json={"count_by":"title", "keyword":""}).json()["count"]

            # create notes
            notes = {"title":self.random_string(10), "content":self.random_string(20), "tags":self.random_string(10)}
            status_code = requests.put(f"{url}/api/notes", headers=header, json=notes).status_code
            assert status_code in [200, 201], "Cannot Create Note" 

            # get notes
            all_notes = requests.get(f"{url}/api/notes").json()
            note = list(filter(lambda x: x["title"] == notes["title"], all_notes))
            assert len(note) != 0, "Note was not created"

            # get new count
            new_count = requests.post(f"{url}/api/notes/count", headers=header, json={"count_by":"title", "keyword":""}).json()["count"]
            assert old_count != new_count, "Invalid count"

            # update notes
            new_content = self.random_string(20)
            notes["id"] = note[0]["id"]
            notes["content"] = new_content
            status_code = requests.patch(f"{url}/api/notes", headers=header, json=notes).status_code
            assert status_code in [200, 204], "Cannot Update Note" 

            # delete notes
            status_code = requests.delete(f"{url}/api/notes/{notes['id']}", headers=header, json=notes).status_code
            assert status_code == 200, "Cannot Delete Note"

            return True

        except Exception as e:
            self.logger.error(f'Could not check gemas-notes: {e}')
            return False
