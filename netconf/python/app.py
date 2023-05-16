#!/usr/bin/env python3

import asyncio
import logging
import signal
import sys
import re

import sysrepo
from pyroute2 import netns
from pyroute2 import IPRoute
from sysrepo import ChangeCreated, ChangeDeleted

def main():
    logging.basicConfig(level=logging.WARNING)
    sysrepo.configure_logging(py_logging=True)

    event_loop = asyncio.get_event_loop()
    finish = asyncio.Event()
    event_loop.add_signal_handler(signal.SIGINT, finish.set)
    event_loop.add_signal_handler(signal.SIGTERM, finish.set)

    try:
        with sysrepo.SysrepoConnection() as conn:
            with conn.start_session() as sess:
                logging.info("subscribe_module_change for openconfig-network-instance")
                sess.subscribe_module_change("openconfig-network-instance",
                                             None,
                                             module_change_cb, asyncio_register=True)
                event_loop.run_until_complete(finish.wait())
        return 0
    except sysrepo.SysrepoError as e:
        logging.error("%s", e)
        return 1

async def module_change_cb(event, req_id, changes, private_data):
    print("Module change event: %s (id %s)" % (event, req_id))

    match event:
        case 'change':
            handle_change(changes)
        case 'done':
            pass
        case _:
            print("Unhandled event %s" % (event))

    await asyncio.sleep(0)

def handle_change(changes):
    for c in changes:
        segments = re.split('/|:|\[|=\'|\']/?', c.xpath);
        match segments:
            case [_, namespace, container, 'network-instance', 'name', name, '']:
                handle_network_instance(name, c)
            case _:
                # ignore
                pass

def handle_network_instance(name, change):
    match change:
        case ChangeCreated():
            print(f"Create network-instance {name}")
            netns.create(name)
            with IPRoute() as ipr:
                ipr.link('add', ifname=f"opi-{name}", kind='veth', peer='veth0')
                (peer,) = ipr.poll(ipr.link, 'dump', timeout=5, ifname='veth0')
                ipr.link('set', index=peer['index'], net_ns_fd=name)
        case ChangeDeleted():
            print(f"Delete network-instance {name}")
            netns.remove(name)
        case _:
            print("Ignoring ...")

if __name__ == "__main__":
    sys.exit(main())
