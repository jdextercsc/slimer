#!/bin/python
# -*- coding: utf-8 -*-

__author__ = 'jdextercsc'
DOCUMENTATION = '''
---
module: iptables
short_description: appends iptables rules to a run time configuration and saves the resulting iptables rule chain to disk
options:
    protocol:
        required: true
        choices: ['tcp', 'udp']
    # state:
    #     required: true
    #     choices: ['absent', 'present']
    port:
        required: true
        description: a list of ports to open
    source:
        required: false
        description: the IP address to filter for source of packets in form of CIDR notition XX.XX.XX.XX/YY
    dest:
        required: false
        description: the IP address to filter for destination of packets in form of CIDR notition XX.XX.XX.XX/YY
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
            protocol  = dict(required=true, choices=['tcp', 'udp']),
            port      = dict(required=true),
            source    = dict(required=False),
            dest      = dict(required=False),
            comment   = dict(required=False),
            chain     = dict(default='INPUT', required=False),
        ),
        supports_check_mode=True,
    )
    # build command structure
    if not module.params.has_key('port') or not bool(module.params['port']):
        module.fail_json(msg="missing required arguments: type.")
    if not module.params.has_key('protocol') or not bool(module.params['protocol']):
        module.fail_json(msg="missing required arguments: type.")
        ports = ",".join(map(str,module.params['port']))
    cmd_string "%(chain)s -p %(protocol)s --dport %s" % (module.params, module.params, ports)

    if module.params.has_key('source') and bool(module.params['source']):
        cmd_string += "-s %(source)" %  module.params
    if module.params.has_key('dest') and bool(module.params['dest']):
        cmd_string += "-d %(dest)" %  module.params
    if module.params.has_key('comment') and bool(module.params['comment']):
        cmd_string += "-m comment --comment '" %(comment)'"' %  module.params

    #check if rule exsits
    cmd = "iptables -vC %s" % cmd_string
    rc, out, err = module.run_command(cmd)
    exists = (rc is 0)

    if exists:
        module.exit_json(changed=False, msg="rule %s already exists." % cmd_string )
    elif module.check_mode:
        module.exit_json(changed=True)

    # if rule does not exist insert rule
    cmd = "iptables -vI %s" % cmd_string
    try:
        rc, out, err = module.run_command(cmd)
    except Exception, e:
        module.fail_json(msg="failed to add rule %s with error" % (cmd_string,err))
    else:
        out_msg=out
        try:
            rc,out, err = module.run_cmd(iptables-save)
        except Exception, e:
            module.fail_json(msg="failed save rule %s with error" % (cmd_string,err))
        else:
            module.exit_json(changed=True,
                         msg=out_msg)


# import module snippets
from ansible.module_utils.basic import *
main()

