#!/usr/bin/python

DOCUMENTATION = '''
module: codepicnic_command
short_description: Execute commands in CodePicnic consoles 
description:
    - This module executes commands using the CodePicnic API as per https://codepicnic.com/docs/api .
version_added: "0.1"
author: "Hector Paz, @hdanniel"
notes:
    - Before execute a command in a console you need to get a valid CodePicnic token. 
    - Only paid accounts have access to the CodePicnic API
options:
    name:
        description:
            - A description of the command to be executed 
        required: false 
        default: null 
    access_token:
        description:
            - CodePicnic Token generated using the module codepicnic_facts
        required: true
        default: null 
    command:
        description:
            - Command to be executed
        required: true 
        default: null 
    container_name:
        description: 
            - a unique name associated with the console
        required: true 
        default: null 
'''

EXAMPLES = '''
- action: codepicnic_name access_token="{{ codepicnic_access_token }}" container_name="7fed342e2f2999fa6802c31af340dcc9e33dedafc994cfbeadf3365927700ca6" command="apt-get install nginx" 
'''

RETURN = '''
{result of command}:
    description: result of command 
    type: string
    sample: "success"
'''


import json
import requests

#requests.packages.urllib3.disable_warnings()

def main():
    module = AnsibleModule(
        argument_spec = dict(
            access_token = dict(required=True),
            container_name = dict(required=True),
            command = dict(required=True)
        )
    )
    cp_api_command_url = 'https://codepicnic.com/api/consoles/'+ module.params['container_name'] + '/exec'
    cp_headers = {'Authorization': 'Bearer ' + module.params['access_token'], 'content-type': 'application/json'}
    cp_bite ={"commands":[module.params['command']]}
    try: 
        cp_command_response = requests.post(cp_api_command_url, data=json.dumps(cp_bite), headers=cp_headers)
    except requests.exceptions.ConnectionError as e:
        module.fail_json(msg="Name or service not known:" + module.params['api_url'])

    try: 
        cp_command_dict = cp_command_response.json()
    except ValueError:
        module.fail_json(msg="Please verify if the CodePicnic API is working")

    if 'error' in  cp_command_dict:
        module.fail_json(msg=cp_command_dict['error_description'])
    if 'error_code' in  cp_command_dict:
        module.fail_json(msg=cp_command_dict['error_message'])

    cp_command_dict['changed'] = True 
    module.exit_json(**cp_command_dict)

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *
if __name__ == '__main__':
        main()
