#!/usr/bin/env python3

import sysrepo
import json
import signal

def module_change_cb(event, req_id, changes, private_data):
    print("Module changed event: %s (request ID %s)" % (event, req_id))
    for c in changes:
        print(repr(c))

with sysrepo.SysrepoConnection() as conn:
    with conn.start_session() as sess:
        sess.subscribe_module_change("openconfig-network-instance", None, module_change_cb)
        signal.sigwait({signal.SIGINT, signal.SIGTERM})
