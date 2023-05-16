#!/usr/bin/env python

from pyroute2 import netns
from pyroute2 import IPRoute

name = 'test'

netns.create(name)

with IPRoute() as ipr:
    ipr.link('add', ifname=name, kind='veth', peer='veth0')

    (peer,) = ipr.poll(ipr.link, 'dump', timeout=5, ifname='veth0')

    ipr.link('set', index=peer['index'], net_ns_fd=name)

