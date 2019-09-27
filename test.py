import requests
import json


class ArchiveSpace:
    def __init__(self, url='http://localhost:8089', user='admin', password='admin'):
        self.base_url = url
        self.username = user
        self.password = password
        self.headers = {'X-ArchivesSpace-Session': self.authenticate()}

    def authenticate(self):
        r = requests.post(url=f'{self.base_url}/users/{self.username}/login?password={self.password}')
        return r.json()['session']

    def create_repository(self, repo_code, repo_name):
        my_new_repository = {
                                  "lock_version": 0,
                                  "repo_code": repo_code,
                                  "name": repo_name,
                                  "created_by": self.username,
                                  "last_modified_by": self.username,
                                  "create_time": "2018-11-26T20:18:07Z",
                                  "system_mtime": "2018-11-26T20:18:07Z",
                                  "user_mtime": "2018-11-26T20:18:07Z",
                                  "publish": True,
                                  "oai_is_disabled": False,
                                  "jsonmodel_type": "repository",
                                  "agent_representation": {
                                      "ref": "/agents/corporate_entities/1"
                                  }
                              }
        r = requests.post(url=f'{self.base_url}/repositories',
                          headers=self.headers,
                          data=json.dumps(my_new_repository))
        return

    def get_repository(self, repo_code):
        r = requests.get(url=f'{self.base_url}/repositories/{repo_code}',
                         headers=self.headers,)
        return r.json()

    def give_me_the_repo_name(self, repo_code):
        r = requests.get(url=f'{self.base_url}/repositories/{repo_code}',
                         headers=self.headers, )
        return r.json()['name']


if __name__ == "__main__":
    kevins_archivespace = ArchiveSpace()
    print(kevins_archivespace.get_repository(2))
