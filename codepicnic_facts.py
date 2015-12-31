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
dest:
    description: destination file/path
    returned: success
    type: string
    sample: "/path/to/file.txt"
src:
    description: source file used for the copy on the target machine
    returned: changed
    type: string
    sample: "/home/httpd/.ansible/tmp/ansible-tmp-1423796390.97-147729857856000/source"
md5sum:
    description: md5 checksum of the file after running copy
    returned: when supported
    type: string
    sample: "2a5aeecc61dc98c4d780b14b330e3282"
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
