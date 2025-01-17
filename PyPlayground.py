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

    def get_first_page_of_objects(self):
        r = requests.get(f'{self.base_url}')
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

    def link_archival_object_to_digital_object(self,
                                               repo_id,
                                               archival_object_id,
                                               digital_object_id):
        """Links an archival object to an existing digital object.

        This method takes an archival object id and a digital object id and links them together. To do this, we
        create a dictionary called digital_object that stores a link to the existing digital object id.  We also
        create a variable called existing_object that stores the existing archival object based on its archival
        object id. We then append the instances list inside the existing_object with our new digital_object dictionary.
        Finally, we use the update an archival object API to push this update to ArchivesSpace.

        Args:
            repo_id (int): The repository id of your ArchivesSpace repository.
            archival_object_id (int): The id of our archival object.
            digital_object_id (int): The id of our digital object.

        Returns:
            dict: A dictionary with messaging about whether or not this worked.

        Examples:
            >>> ArchiveSpace.link_archival_object_to_digital_object(2, 6278, 602)
            {'status': 'Updated', 'id': 6278, 'lock_version': 1, 'stale': True, 'uri':
            '/repositories/2/archival_objects/6278', 'warnings': []}

        """
        digital_object = {
            'is_representative': True,
            'instance_type': 'digital_object',
            'jsonmodel_type': 'instance',
            'digital_object': {
                'ref': f'/repositories/2/digital_objects/{digital_object_id}'
            }
        }
        existing_object = self.get_archival_object(
            id=archival_object_id,
            repo_id=repo_id
        )
        existing_object['instances'].append(digital_object)
        r = requests.post(url=f'{self.base_url}/repositories/{repo_id}/archival_objects/{archival_object_id}',
                          headers=self.headers,
                          data=json.dumps(existing_object))
        return r.json()

    def link_digital_object_to_a_collection(self,
                                            repo_id,
                                            resource_id,
                                            digital_object_id):
        digital_object = {
            'is_representative': False,
            'instance_type': 'digital_object',
            'jsonmodel_type': 'instance',
            'digital_object': {
                'ref': f'/repositories/2/digital_objects/{digital_object_id}'
            }
        }
        existing_collection = self.get_a_resource(repo_id, resource_id)
        existing_collection['instances'].append(digital_object)
        r = requests.post(url=f'{self.base_url}/repositories/{repo_id}/resources/{resource_id}',
                          headers=self.headers,
                          data=json.dumps(existing_collection))
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

    def getresources(self, repo_id):
        r = requests.get(
            url=f'{self.base_url}/repositories/{repo_id}/resources?page=2&page_size=1',
            headers=self.headers,
        )
        return r.json()

    def get_a_resource(self, repo_id, resource_id):
        r = requests.get(
            url=f'{self.base_url}/repositories/{repo_id}/resources/{resource_id}',
            headers=self.headers,
        )
        return r.json()

    def get_associated_archival_objects(self, repo_id, resource_id):
        r = requests.get(
            url=f'{self.base_url}/repositories/{repo_id}/resources/{resource_id}/ordered_records',
            headers=self.headers,
        )
        return r.json()

    def get_a_digital_object(self, repo_id, digital_object_id):
        r = requests.get(
            url=f'{self.base_url}/repositories/{repo_id}/digital_objects/{digital_object_id}',
            headers=self.headers,
        )
        return r.json()

    def create_a_digital_object(self,
                                repo_id,
                                digital_object_id,
                                url,
                                title
                                ):
        """Creates a digital object.

        This takes a repo id , the id of a digital object, a url , and a title and creates a digital object in
        ArchivesSpace.

        Args:
            repo_id(int): The id of a repository in ArchivesSpace.
            digital_object_id (str): A unique identifer for your new digital object in ArchivesSpace.
            url (str): The url to the digital object in another system.
            title (str): The title of your new digital object.

        Return:
            dict: A dict with the status of your request.

        Examples:
            >>> ArchiveSpace.create_a_digital_object(2, 'abc8776', 'http://google.com', 'The title of my new object')
            {'status': 'Created', 'id': 703, 'lock_version': 0, 'stale': None, 'uri': '/repositories/2/digital_objects/703', 'warnings': []}
            >>> ArchiveSpace.create_a_digital_object(2, 'abc8776', 'http://google.com', 'The title of my new object')
            {'error': {'digital_object_id': ['Must be unique']}}

        """
        my_dictionary = {
            "jsonmodel_type": "digital_object",
            "external_ids": [],
            "subjects": [],
            "linked_events": [],
            "external_documents":[],
            "rights_statements":[],
            "linked_agents":[],
            "is_slug_auto": True,
            "file_versions":[
                { "jsonmodel_type":"file_version",
                  "is_representative": True,
                  "file_uri": url,
                  "xlink_actuate_attribute":"onRequest",
                  "xlink_show_attribute":"new",
                  "publish": True}],
            "restrictions": False,
            "notes":[],
            "linked_instances":[],
            "title": title,
            "digital_object_id": digital_object_id
        }
        r = requests.post(url=f'{self.base_url}/repositories/{repo_id}/digital_objects',
                          headers=self.headers,
                          data=json.dumps(my_dictionary))
        return r.json()

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
    #webster = AncestorsSolrSearch().get_first_page_of_objects()
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

    # list_of_archival_objects = kevins_archivespace.get_list_of_archival_objects_in_repository(2)
    # for archival_object in tqdm(list_of_archival_objects):
    #     kevins_archivespace.replace_comma_at_end(archival_object)
    # print(
    #     kevins_archivespace.get_associated_archival_objects(
    #         2,
    #         13
    #     )
    # )
    # print(
    #     kevins_archivespace.get_a_resource(2, 13)
    # )
    # print(
    #     kevins_archivespace.get_a_digital_object(
    #         repo_id=2,
    #         digital_object_id=601
    #     )
    # )
    # print(
    #     kevins_archivespace.create_a_digital_object(
    #         repo_id=2,
    #         digital_object_id='0012_002333_000711_0001',
    #         url='https://digital.lib.utk.edu/collections/islandora/object/webster:1460',
    #         title='#434: Rainbow Falls'
    #     )
    # )
    # print(
    #     kevins_archivespace.get_archival_object(
    #         id=5763,
    #         repo_id=2
    #     )
    # )
    # print(
    #     kevins_archivespace.link_archival_object_to_digital_object(
    #         repo_id=2,
    #         archival_object_id=6278,
    #         digital_object_id=602
    #     )
    # )
    # with open('output.json', 'w') as my_file:
    #     my_file.write(str(kevins_archivespace.get_associated_archival_objects(2, 13)))

    def link_webster_objects():
        our_archival_objects = []
        i = 0
        for archical_object in kevins_archivespace.get_associated_archival_objects(2,13)['uris']:
            if i != 0:
                our_archival_objects.append(archical_object)
            i += 1
        all_titles = [x['display_string'] for x in our_archival_objects if x['ref'].rfind('archival_objects') != -1]
        for x in our_archival_objects:
            title = x['display_string'].split(',,')[0]
            archival_object_id = x['ref'].split('/')[4]
            occurences = all_titles.count(x['display_string'])
            for digital_object in webster:
                if digital_object['mods_note_s'] == title:
                    # print(digital_object)
                    print(status)
                    status = kevins_archivespace.create_a_digital_object(2,
                                                                        digital_object['mods_identifier_local_s'],
                                                                        f'https://digital.lib.utk.edu/collections/islandora/object/{digital_object["PID"]}',
                                                                        digital_object['mods_note_s'])
                    try:
                        if status['status'] == "Created" and occurences == 1:
                            kevins_archivespace.link_archival_object_to_digital_object(2,
                                                                                       archival_object_id,
                                                                                       status['id'])
                            break
                    except KeyError:
                        break
    #
    # print(kevins_archivespace.create_a_digital_object(2, 'abcdefghijk', 'http://google.com', 'Delete me'))

    def link_solr_objects_to_collection(solr_objects, collection_id):
        """Creates digital objects in a space and links to an a-space collection

         Requires a list of solr objects and creates a digital object for each item in list and links to a collection
         in aspace

        Args:
             solr_objects (list): A list of Solr objects from Islandora as dicts with the PID, the identifier, and title
             of the object
             collection_id (int): the number that represents a collection in Archives Space

        Returns:
            dict: a dict with a list of key errors that happened and the digital objects that were successfully linked

        """
        errors = []
        successes = []
        for item in tqdm(solr_objects):c
            status = kevins_archivespace.create_a_digital_object(2,
                                                                 item['mods_identifier_local_s'],
                                                                 f'https://digital.lib.utk.edu/collections/islandora/object/{item["PID"]}',
                                                                 item['mods_note_s'])
            try:
                if status['status'] == 'Created':
                    kevins_archivespace.link_digital_object_to_a_collection(2,collection_id,status['id'])
                    successes.append(status['id'])
            except KeyError:
                errors.append(item)
                pass
        return {"errors": errors, }

     # print(kevins_archivespace.link_digital_object_to_a_collection(2, 13, 760))
    sample = {'responseHeader': {'status': 0, 'QTime': 86, 'params': {'q': 'ancestors_ms:"gsmrc:webster"', 'indent': 'true', 'fl': 'mods_note_s,mods_identifier_local_s,PID', 'wt': 'json'}}, 'response': {'numFound': 514, 'start': 0, 'docs': [{'PID': 'webster:1052', 'mods_note_s': '#27: Cabin at Three Forks', 'mods_identifier_local_s': '0012_002333_000229_0001'}, {'PID': 'webster:1020', 'mods_note_s': '#9: View from House Mountain', 'mods_identifier_local_s': '0012_002333_000211_0001'}, {'PID': 'webster:1072', 'mods_note_s': "#78: Group at Major Campbell's", 'mods_identifier_local_s': '0012_002333_000288_0001'}, {'PID': 'webster:1132', 'mods_note_s': '#130: The Barn', 'mods_identifier_local_s': '0012_002333_000345_0001'}, {'PID': 'webster:1134', 'mods_note_s': '#132: Down Roaring Fork with Dutch Roth, Harvey Broome, Harris [?], & Sonny Morris', 'mods_identifier_local_s': '0012_002333_000347_0001'}, {'PID': 'webster:1135', 'mods_note_s': '#133: Sheep at Standing Indian', 'mods_identifier_local_s': '0012_002333_000348_0001'}, {'PID': 'webster:1133', 'mods_note_s': '#131: Self at odd shaped tree near Strattons Bald', 'mods_identifier_local_s': '0012_002333_000346_0001'}, {'PID': 'webster:1137', 'mods_note_s': '#135: State Line', 'mods_identifier_local_s': '0012_002333_000351_0001'}, {'PID': 'webster:1136', 'mods_note_s': '#134: Little fall on Ekaneekle Creek on return from Gregory', 'mods_identifier_local_s': '0012_002333_000349_0001'}, {'PID': 'webster:1139', 'mods_note_s': '#136: Tub Mill on Ramsey Prong - Greenbrier. Special', 'mods_identifier_local_s': '0012_002333_000353_0001'}]}}
    print(link_solr_objects_to_collection(sample['response']['docs'], 6))
