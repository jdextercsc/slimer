#!/bin/python
# -*- coding: utf-8 -*-

__author__ = 'jdextercsc'
DOCUMENTATION = '''
---
module: iptables
short_description: appends iptables rules to a run time configuration and saves the resulting iptables rule chain to disk
options:
    protocol:
        required: false
        default: 'tcp'
        choices: ['tcp', 'udp']
    # state:
    #     required: true
    #     choices: ['absent', 'present']
    port:
        required: true
        description: a list of ports to open
    source:
        required: false
        description: the IP address to filter for source of packets in form of CIDR notation XX.XX.XX.XX/YY
    dest:
        required: false
        description: the IP address to filter for destination of packets in form of CIDR notation XX.XX.XX.XX/YY
    comment:
        required: false
        description: a string containing a descriptive comment about the rule.
    chain:
        required: false
        default: 'INPUT'

'''

def main():
    module = AnsibleModule(
        argument_spec = dict(
            # state     = dict(required=true, choices=['absent', 'present']),
            protocol  = dict(required=False, default='tcp', choices=['tcp', 'udp']),
            port      = dict(required=True),
            source    = dict(required=False),
            dest      = dict(required=False),
            comment   = dict(required=False),
            chain     = dict(default='INPUT', required=False),
        ),
        supports_check_mode=True,
    )
    ports = module.params['port']
    if isinstance(ports, list):
        ports = ",".join(map(str, ports))
    	cmd_string = "%(chain)s" % module.params
        cmd_string +=" -p %(protocol)s" % module.params
        cmd_string +=" -m multiport --dport %s" % ports
    else:
        cmd_string = "%(chain)s -p %(protocol)s --dport %(port)s" %  module.params
    if module.params.has_key('source') and bool(module.params['source']):
        cmd_string += " -s %(source)s" %  module.params
    if module.params.has_key('dest') and bool(module.params['dest']):
        cmd_string += " -d %(dest)s" %  module.params
    if module.params.has_key('comment') and bool(module.params['comment']):
        cmd_string += ' -m comment --comment " %(comment)s"' %  module.params
    
    #check if rule exsits
    cmd = "iptables -vC %s -j ACCEPT" % cmd_string
    rc, out, err = module.run_command(cmd)
    if rc is 0:
        module.exit_json(changed=False, msg="rule %s already exists." % cmd_string )
    elif rc is 2:
        module.fail_json(msg=err)
    elif rc is 1 and module.check_mode:
        module.exit_json(changed=True)

    # if rule does not exist insert rule
    cmd = "iptables -vI %s -j ACCEPT" % cmd_string
    rc, out, err = module.run_command(cmd)
    if rc is 1:
    	module.fail_json(msg="failed to add rule %s with error %s" % (cmd_string,err))
    else:
        cmd = 'service iptables save'
        rc, out, err = module.run_command(cmd)
        
        if rc is 1:
            module.fail_json(msg=err)
        else:
            module.exit_json(changed=True, msg=cmd_string)


from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()