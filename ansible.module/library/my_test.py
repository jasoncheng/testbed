#!/usr/bin/python
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
DOCUMENTATION = r'''
---
module: my_test

hello world
'''
EXAMPLES = r'''
- name: test0
  my_namespace.my_collection.my_test:
    name: hello world

- name: test2
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

- name: hello
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
original_message:
  description: the original name param that was passed in
  type: str
  returned: always
  sample: 'hello world'
message:
  description: the output message that the test module generates.
  type: str
  returned: always
  sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        name=dict(type='str', require=True),
        new=dict(type='bool', require=False, default=False)
    )
    result = dict(
        changed=False,
        original_message = '',
        message=''
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
    
    if module.check_mode:
        module.exit_json(**result)
        
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'
    
    if module.params['new']:
        result['changed'] = True
        
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)
        
    module.exit_json(**result)
    
def main():
    run_module()
    
if __name__ == '__main__':
    main()