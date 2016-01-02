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

You can try the modules with our [Demo CodePicnic console](https://codepicnic.com/consoles/my-ansible-console-2-1451740901/embed) :
- Open the console
- Enter your credentials into the file ansible-codepicnic/playbook-example.yaml
- Execute the following command:

    ansible-playbook ansible-codepicnic/playbook-example.yaml -M ansible-codepicnic/ -i ansible-codepicnic/hosts-example 


