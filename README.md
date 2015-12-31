# ansible-codepicnic
Ansible Modules for [CodePicnic.com](https://codepicnic.com/docs/api "CodePicnic API")

## codepicnic_facts
Generate the authentication token using the application credentials

## codepicnic_console
Create a new CodePicnic console

## Example

- name: CodePicnic consoles
  hosts: localhost
  tasks:
  	- name: Gather CodePicnic facts
      codepicnic_facts:
         client_id=f6a67f7306211a947ce7f061284c7e0474f84c5044f1968b92d5320112 
         client_secret=e15414ab5f0e3dc299c3e5e1fce1abe6768a8de1ea593e1bde514583
    - name: Create CodePicnic console
      codepicnic_console:
      	 access_token="{{ codepicnic_access_token }}"
         size="medium"
         type="python"
         title="my ansible console"
         