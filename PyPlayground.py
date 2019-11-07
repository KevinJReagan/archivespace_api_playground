import requests
import json
from tqdm import tqdm


class AncestorsSolrSearch:
    def __init__(self,
                 url="http://porter.lib.utk.edu:8080",
                 ancestor="gsmrc:webster",
                 solr_fields='mods_note_s,mods_identifier_local_s,PID'
                 ):
        self.base_url = f'{url}/solr/collection1/select?q=ancestors_ms:"{ancestor}"&fl={solr_fields}&wt=json&indent=true'
        self.rows = self.get_rows()

    def get_rows(self):
        r = requests.get(self.base_url)
        return r.json()['response']['numFound']

    def get_all_digital_objects(self):
        r = requests.get(f'{self.base_url}&rows={self.rows}')
        return r.json()['response']['docs']


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

    def get_list_of_archival_objects_in_repository(self, repo_id):
        """ Lists numbers of archival objects in Repository in Archives Space

        Args:
            repo_id (int): repository ID you want to use

        Returns:
            list: a list of integers for each archival object

        Examples:
            >>> ArchiveSpace.get_list_of_archival_objects_in_repository(2)
            [1,2,3,4,5,6]

        """
        search_string = f'{self.base_url}/repositories/{repo_id}/archival_objects?all_ids=true'
        r = requests.get(
            url=search_string,
            headers=self.headers
                )
        return r.json()

    def replace_comma_at_end(self, archival_object_id, repo_id=2):
        """Replace comma at end of an archival objects title if it exists.

        This method replaces the comma at the end of the title of an archival object if it exists.  This requires
        the id of an archival object and optionally accepts the id of an ArchivesSpace repository.  The default
        value is 2.

        Args:
            archival_object_id (int): The id of an Archival Object in ArchivesSpace.
            repo_id (int): The id of the repository in ArchivesSpace.  2 by default.

        Returns:
            str: The status of the request or "No comma at end of title." If successful, the str should be "Updated."

        Examples:
            >>> ArchiveSpace().replace_comma_at_end(5630, 2)
            'Updated'
            >>> ArchiveSpace().replace_comma_at_end(5630, 2)
            'No comma at end of title.'

        """
        metadata_from_archival_object = self.get_archival_object(archival_object_id, repo_id)
        title = metadata_from_archival_object['title']
        if title.endswith(','):
            title = title[:-1]
            metadata_from_archival_object['title'] = title
            r = requests.post(
                url=f'{self.base_url}/repositories/{repo_id}/archival_objects/{archival_object_id}',
                headers=self.headers,
                data=json.dumps(metadata_from_archival_object)
            )
            return r.json()['status']
        else:
            return "No comma at end of title."


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

    list_of_archival_objects = kevins_archivespace.get_list_of_archival_objects_in_repository(2)
    for archival_object in tqdm(list_of_archival_objects):
        kevins_archivespace.replace_comma_at_end(archival_object)
