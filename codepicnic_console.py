#!/usr/bin/python

import json
import requests
import requests.packages.urllib3
import pprint

requests.packages.urllib3.disable_warnings()

def main():
    module = AnsibleModule(
        argument_spec = dict(
            access_token = dict(required=True),
            size = dict(required=True),
            type = dict(required=True),
            hostname = dict(default=''),
            title = dict(default=''),
            custom_image = dict(default=''),
            api_url = dict (default='https://codepicnic.com/api/consoles')
        )
    )
    cp_headers = {'Authorization': 'Bearer ' + module.params['access_token'], 'content-type': 'application/json'}
    cp_bite ={"bite":{"container_size":module.params['size'], "container_type":module.params['type'], "hostname":module.params['hostname'], "title":module.params['title']}}
    try: 
        cp_token_response = requests.post(module.params['api_url'], data=json.dumps(cp_bite), headers=cp_headers)
    except requests.exceptions.ConnectionError as e:
        module.fail_json(msg="Name or service not known:" + module.params['api_url'])

    #if cp_token_response.status_code != 200: 
    #    module.fail_json(msg="Please verify if the CodePicnic API is working - Status: " + str(cp_token_response.status_code))
    
    cp_token_dict = cp_token_response.json()
    if 'error' in  cp_token_dict:
        module.fail_json(msg=cp_token_dict['error_description'])

    cp_token_dict['changed'] = True 
    #cp_token_dict['ansible_facts'] = dict(codepicnic_access_token=cp_token_dict['access_token'])
    module.exit_json(**cp_token_dict)

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
if __name__ == '__main__':
        main()
