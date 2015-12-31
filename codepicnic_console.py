#!/usr/bin/python

DOCUMENTATION = '''
module: codepicnic_console
short_description: Create new CodePicnic consoles 
description:
    - This module creates new consoles using the CodePicnic API as per https://codepicnic.com/docs/api .
      The module returns the URL of the new console
version_added: "0.1"
author: "Hector Paz, @hdanniel"
notes:
    - Before create a console you need to get a valid CodePicnic token. 
    - Only paid accounts have access to the CodePicnic API 
options:
    title:
        description:
            - Name of the new Console
        alias: name 
        required: false 
        default: null 
    access_token:
        description:
            - CodePicnic Token generated using the module codepicnic_facts
        required: true
        default: null 
    size:
        description:
            - Container size from the following options: medium (256 MB), large (512 MB), xlarge (1 GB) or xxlarge (3 GB) 
        required: true 
        default: medium
    type:
        description:
            - Container type from the following options: bash, js, mono, elixir, go, nodejs, php, python, python340, python350, ruby, dancer, laravel, phoenix, rails, mongodb, redis 
        required: true 
        default: bash 
    hostname:
        description:
            - Name to be used as console hostname: user@your_custom_hostname 
        required: false 
        default: null 

'''

EXAMPLES = '''
- action: codepicnic_console title='MY NEW CONSOLE NAME' access_token="{{ codepicnic_access_token }}" size='medium' type='python' hostname='MY_NEW_CONSOLE'
'''

RETURN = '''
container_name:
    description: an unique identifier associated with your console, 
    type: string
    sample: "7fed342e2f2999fa6802c31af340dcc9e33dedafc994cfbeadf3365927700ca6"
url:
    description: url of the new console 
    returned: changed
    type: string
    sample: "http://codepicnic.com/consoles/MTU4NzM4/embed"
'''


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
