#!/usr/bin/python
DOCUMENTATION = '''
module: codepicnic_facts 
short_description: Gathers facts about CodePicnic account 
description:
    - This module fetches data from the CodePicnic API as per https://codepicnic.com/docs/api .
      The module returns the generated token from your CodePicnic credentials.
version_added: "0.1"
author: "Hector Paz, @hdanniel"
notes:
    - Only paid accounts have access to the CodePicnic API 
options:
    client_id:
        description:
            - Application ID from your CodePicnic account 
        required: true
        default: null 
    client_secret:
        description:
            - Secret Key from your CodePicnic account 
        required: true
        default: null 

'''

EXAMPLES = '''
- action: codepicnic_facts client_id=YOUR_CODEPICNIC_APPLICATION_ID client_secret=YOUR_CODEPICNIC_SECRET_KEY 
'''

RETURN = '''
codepicnic_access_token:
    description: generated token to be used in following actions 
    returned: success
    type: string
    sample: "c12ab983a9d15eb7c522eacf01c164ad04f25c74ba54024f2639a6f88e91c935"
'''

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
    cp_token_dict['ansible_facts'] = dict(codepicnic_access_token=cp_token_dict['access_token'])
    module.exit_json(**cp_token_dict)

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
if __name__ == '__main__':
        main()
