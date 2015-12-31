# ansible-codepicnic
Ansible Modules for [CodePicnic.com](https://codepicnic.com/docs/api "CodePicnic API")

## codepicnic_facts
Generate the authentication token using the application credentials

## codepicnic_console
Create a new CodePicnic console

## Playbook example

    - name: CodePicnic consoles
      hosts: localhost
      tasks:
  	  - name: Gather CodePicnic facts
        codepicnic_facts:
            client_id=XXXXXXXXXXXXXXXXXXXXXXX 
            client_secret=YYYYYYYYYYYYYYYYYYYYYYYYYYYY
      - name: Create CodePicnic console
        codepicnic_console:
      	    access_token="{{ codepicnic_access_token }}"
            size="medium"
            type="python"
            title="my ansible console"
         