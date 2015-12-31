#!/usr/bin/python

import json
import requests
import requests.packages.urllib3
import pprint

requests.packages.urllib3.disable_warnings()

def main():
    module = AnsibleModule(
        argument_spec = dict(
            title = dict(default='',aliases=['name']),
            access_token = dict(required=True),
            size = dict(required=True),
            type = dict(required=True),
            hostname = dict(default=''),
            custom_image = dict(default=''),
            api_url = dict (default='https://codepicnic.com/api/consoles')
        )
    )
    cp_headers = {'Authorization': 'Bearer ' + module.params['access_token'], 'content-type': 'application/json'}
    cp_bite ={"bite":{"container_size":module.params['size'], "container_type":module.params['type'], "hostname":module.params['hostname'], "title":module.params['title']}}
    try: 
        cp_console_response = requests.post(module.params['api_url'], data=json.dumps(cp_bite), headers=cp_headers)
    except requests.exceptions.ConnectionError as e:
        module.fail_json(msg="Name or service not known:" + module.params['api_url'])

    #if cp_token_response.status_code != 200: 
    #    module.fail_json(msg="Please verify if the CodePicnic API is working - Status: " + str(cp_token_response.status_code))
    
    try: 
        cp_console_dict = cp_console_response.json()
    except ValueError:
        module.fail_json(msg="Please verify if the CodePicnic API is working")

    if 'error' in  cp_console_dict:
        module.fail_json(msg=cp_console_dict['error_description'])
    if 'error_code' in  cp_console_dict:
        module.fail_json(msg=cp_console_dict['error_message'])

    cp_console_dict['changed'] = True 
    module.exit_json(**cp_console_dict)

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
if __name__ == '__main__':
        main()
