#!/usr/bin/env python3

import sysrepo
import json

with sysrepo.SysrepoConnection() as conn:
    with conn.start_session("running") as sess:
        data = sess.get_data("/network-instances")
        print(json.dumps(data))
