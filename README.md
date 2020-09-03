# Ansible swrole become plugin for RBAC-enabled AIX

Ansible uses a system of become plugins for privilege escalation and has a lot of such plugins in the standard distribution. AIX has its own system of privilege esclation known as Role Based Access Control (RBAC). Enhanced RBAC is available since AIX 6.1 and switched on in the standard AIX installation. This plugin allows to use AIX Enhanced RBAC with Ansible.

## Installation

just copy swrole.py into /opt/freeware/lib/python3.7/site-packages/ansible/plugins/become or where your ansible is installed.

## Options

### ANSIBLE_BECOME_EXE

Path to swrole. Default: /usr/bin/swrole.

### ANSIBLE_BECOME_ROLE

The only required option. The role you want to apply.

### ANSIBLE_BECOME_PASSWORD

Password if your role requires password authentication. **It doesn't work now!**

## Usage example

```
# cat inventory
aixserver

[all:vars]
ansible_python_interpreter=/opt/freeware/bin/python3
ansible_user=user1
ansible_ssh_private_key_file=/home/user1/.ssh/id_rsa
ansible_become=yes
ansible_become_method=swrole
ansible_become_role=aixadmin
# ansible_become_password=password1
```

### Make a role

Please note **auth_mode=NONE** in the line below! Because the plugin doesn't understand password prompt for now, you must switch off the authentication.

```
# mkrole authorizations=aix auth_mode=NONE aixadmin
# setkst
```

### Assign the role to a user

```
# chuser roles=aixadmin user1
```

You can also assign the role as default role to the user:

```
# chuser default_roles=aixadmin user1
```

But in this case you don't need any become plugins. The role is always assigned to the user.
