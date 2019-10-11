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
        print(r.json())
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

    def get_created_by_value_for_this_repo(self, repo_code):
        r = requests.get(url=f'{self.base_url}/repositories/{repo_code}',
                         headers=self.headers, )
        return r.json()['created_by']

    def delete_repo(self, repo_number):
        r = requests.delete(url=f'{self.base_url}/repositories/{repo_number}',
                            headers=self.headers,)
        return r.json()

    def list_all_repositories(self):
        r = requests.get(url=f'{self.base_url}/repositories?page=1&page_size=10',
                            headers=self.headers,)
        return r.json()

    def create_new_user(self, username, password, is_admin=False):
        mydictionary = { "jsonmodel_type":"user",
                         "groups":[],
                         "is_admin": is_admin,
                         "username": username,
                         "name": username}
        r = requests.post(url=f'{self.base_url}/users?password={password}',
                          headers=self.headers,
                          data=json.dumps(mydictionary))
        return r.json()

    def list_users(self):
        r = requests.get(
            url=f'{self.base_url}/users?page=1&page_size=10',
            headers=self.headers
        )
        list_of_usernames = []
        for result in r.json()['results']:
            list_of_usernames.append(result['name'])
        return list_of_usernames

    def remove_user(self, user_id):
        r = requests.delete(
            url=f'{self.base_url}/users/{user_id}',
            headers=self.headers
        )
        return r.json()

    def user_details(self, user_id):
        r= requests.get(
            url=f'{self.base_url}/users/{user_id}',
            headers=self.headers
        )
        return r.json()

    def get_subject_id(self, subject_id):
        r = requests.get(
            url=f'{self.base_url}/subjects/{subject_id}', headers=self.headers)
        return r.json()

    def delete_subject(self, delete_subj_id):
        r = requests.delete(url=f'{self.base_url}/subjects/{delete_subj_id}',
            headers=self.headers)
        return r.json()

    def get_a_person(self, person_agent_id):
        r = requests.get(
            url=f'{self.base_url}/agents/people/{person_agent_id}',
            headers=self.headers)
        return r.json()

    def get_a_software(self, software_agent_id):
        r = requests.get(
            url=f'{self.base_url}/agents/software/{software_agent_id}',
            headers=self.headers)
        return r.json()

    def get_a_corporate_entity(self, corporate_entity_id):
        r = requests.get(url=f'{self.base_url}/agents/corporate_entities/{corporate_entity_id}',
            headers=self.headers)
        return r.json()

    def get_a_family(self, family_id):
        r = requests.get(
            url=f'{self.base_url}/agents/families/{family_id}',
            headers=self.headers)
        return r.json()

    def delete_a_person(self, delete_person):
        r = requests.delete(
            url=f'{self.base_url}/agents/people/{delete_person}',
            headers=self.headers)
        return r.json()

    def delete_a_software(self, delete_software):
        r = requests.delete(
            url=f'{self.base_url}/agents/software/{delete_software}',
            headers=self.headers)
        return r.json()

    def delete_a_corporate_entity(self, delete_corporate):
        r = requests.delete(
            url=f'{self.base_url}/agents/corporate_entities/{delete_corporate}',
            headers=self.headers)
        return r.json()

    def delete_a_family(self, delete_family):
        r = requests.delete(
            url=f'{self.base_url}/agents/families/{delete_family}',
            headers=self.headers)
        return r.json()

    def get_archival_object(self, id, repo_id):
        r = requests.get(
            url=f'{self.base_url}/repositories/{repo_id}/archival_objects/{id}',
            headers=self.headers)
        return r.json()

    def get_display_string_for_archival_object(self, id, repo_id):
        r = requests.get(
            url=f'{self.base_url}/repositories/{repo_id}/archival_objects/{id}',
            headers=self.headers)
        return r.json()['display_string']

    def get_title_for_archival_object(self, id, repo_id):
        r = requests.get(
            url=f'{self.base_url}/repositories/{repo_id}/archival_objects/{id}',
            headers=self.headers)
        return r.json()['title']

    def get_list_of_archival_objects_in_repository(self, repo_list):
        search_string = f'{self.base_url}/repositories/{repo_list}/archival_objects?all_ids=true'
        r = requests.get(
            url=search_string,
            headers=self.headers
                )
        #print(search_string)
        return r.json()

    def replace_double_commas_in_archival_object(self, id, repo_id=2):
        metadata_from_archival_object = self.get_archival_object(id, repo_id)
        display_string = metadata_from_archival_object['display_string']
        print(display_string)
        new_display_string = display_string.replace(',,', ',')
        print(new_display_string)
        metadata_from_archival_object['display_string'] = new_display_string
        #metadata_from_archival_object["jsonmodel_type"] = "archival_object"
        print(metadata_from_archival_object)
        r = requests.post(
            url=f'{self.base_url}/repositories/{repo_id}/archival_objects/{id}',
            headers=self.headers,
            data=json.dumps(metadata_from_archival_object)
        )
        print(r.status_code)
        return r.json()['status']

    # def get_user_details(self):
    #     r = requests.get("X-ArchivesSpace-Session: $SESSION" "http://localhost:8089/users/1"
    #     )
    #     return j.son()
    # def get_archival_objectby_id(self):
    #     r = requests.get(url=f'{self.base_url} /repositories/:repo_id/archival_objects/:id)")
    #     return j.son)
    # def get_list_of_archival object_by_id
    #
    # def update_archival_object():
    #     r= requests.get(url=f'{self.base_url} /repositories/:repo_id/archival_objects/:id)'
    #                         f'/repositories/:repo_id/archival_objects))'
    # def get_uri
    #     r= requests.get(url=f'{self.base_url} /repositories/:repo_id/archival_objects/:id)')
    #     "X-ArchivesSpace-Session: $SESSION" "http://localhost:8089/repositories/2/jobs/1/records?page=1&page_size=10
    #
    #     return r.json

if __name__ == "__main__":
    kevins_archivespace = ArchiveSpace()
    # print(kevins_archivespace.get_created_by_value_for_this_repo(2))
    #print(kevins_archivespace.list_all_repositories())
    #print(kevins_archivespace.create_new_user("john", "password123"))
    #kevins_archivespace.create_new_user('mark', 'password123')
    #print(kevins_archivespace.list_users())
#   print(kevins_archivespace.remove_user(6))
   # print(kevins_archivespace.user_details(5))
    #print(kevins_archivespace.get_subject_id(11))
   #13 print(kevins_archivespace.get_a_person(117))

#14print(kevins_archivespace.get_a_software(1))
#15print(kevins_archivespace.get_a_corporate_entity(208))
#16print(kevins_archivespace.get_a_family(1))
#17print(kevins_archivespace.delete_a_person(2))
#18 print(kevins_archivespace.delete_a_software(1))
#19print((kevins_archivespace.delete_a_corporate_entity(208)))
#20print(kevins_archivespace.delete_a_family(1))
# print(kevins_archivespace.get_archival_object_id(
#     repo_id=2,
#     id=2
# )
# )
#print(kevins_archivespace.get_list_of_archival_objects_in_repository(2))

    # our_list = kevins_archivespace.get_list_of_archival_objects_in_repository(2)
    # for archival_object_id in our_list:
    #     print(kevins_archivespace.get_display_string_for_archival_object(archival_object_id, 2))

    # kevins_string = "This beer is bad."
    # print(kevins_string.replace('beer','wine'))

    print(
        kevins_archivespace.replace_double_commas_in_archival_object(5630, 2)
    )



