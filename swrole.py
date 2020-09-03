# -*- coding: utf-8 -*-
# Copyright: (c) 2020, eNFence GmbH
# under MIT License (see LICENSE)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    become: swrole
    short_description: AIX RBAC switch role
    description:
        - This become plugins allows your remote/login user to execute commands with an AIX RBAC role via the swrole utility.
    author: eNFence GmbH
    options:
        become_exe:
            description: swrole executable
            default: swrole
            ini:
              - section: privilege_escalation
                key: become_exe
              - section: swrole_become_plugin
                key: executable
            vars:
              - name: ansible_become_exe
              - name: ansible_swrole_exe
            env:
              - name: ANSIBLE_BECOME_EXE
              - name: ANSIBLE_SWROLE_EXE
        become_role:
            description: RBAC role
            required: True
            vars:
              - name: ansible_become_role
              - name: ansible_swrole_role
            env:
              - name: ANSIBLE_BECOME_ROLE
              - name: ANSIBLE_SWROLE_ROLE
            ini:
              - section: swrole_become_plugin
                key: role
        become_pass:
            description: swrole password
            required: False
            vars:
              - name: ansible_become_password
              - name: ansible_become_pass
              - name: ansible_swrole_pass
            env:
              - name: ANSIBLE_BECOME_PASS
              - name: ANSIBLE_SWROLE_PASS
            ini:
              - section: swrole_become_plugin
                key: password
    notes:
      - You must specify the target RBAC role in become_user.
      - As for now it doesn't understand password prompt. Hint: chrole -a auth_mode=NONE rolename.
"""

from ansible.plugins.become import BecomeBase
from ansible.module_utils.six.moves import shlex_quote


class BecomeModule(BecomeBase):

    name = 'swrole'

    def build_become_command(self, cmd, shell):
        super(BecomeModule, self).build_become_command(cmd, shell)

        if not cmd:
            return cmd

        if self.get_option('become_pass'):
            self.prompt = '%s\'s Password:' % self._id
        become = self.get_option('become_exe') or self.name
        role = self.get_option('become_role') or ''
        return '%s %s -c %s' % (become, role, shlex_quote(self._build_success_command(cmd, shell)))
