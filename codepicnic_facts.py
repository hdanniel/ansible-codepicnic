#!/usr/bin/python

import json
import requests
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

def main():
    module = AnsibleModule(
        argument_spec = dict(
            client_id = dict(required=True),
            client_secret = dict(required=True),
            api_url = dict (default='https://codepicnic.com/oauth/token')
        )
    )
    cp_payload = dict(
        grant_type = 'client_credentials',
        client_id = module.params['client_id'],
        client_secret = module.params['client_secret'],
    )
    try: 
        cp_token_response = requests.post(module.params['api_url'], data=cp_payload)
    except requests.exceptions.ConnectionError as e:
        module.fail_json(msg="Name or service not known:" + module.params['api_url'])

    #if cp_token_response.status_code != 200: 
    #    module.fail_json(msg="Please verify if the CodePicnic API is working - Status: " + str(cp_token_response.status_code))
    
    cp_token_dict = cp_token_response.json()
    if 'error' in  cp_token_dict:
        module.fail_json(msg=cp_token_dict['error_description'])

    cp_token_dict['changed'] = True 
    cp_token_dict['ansible_facts'] = dict(codepicnic_token='')
    module.exit_json(**cp_token_dict)

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
if __name__ == '__main__':
        main()
