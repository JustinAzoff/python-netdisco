#!/usr/bin/env python
import sys
import datetime

from netdisco import db as netdisco_db
from netdisco.db import and_

def older_ranges(nodes):
    now = datetime.date.today()
    t = now - datetime.timedelta(days=365)
    d = datetime.timedelta(days=30)

    while t < now - d:
        nodes = [n for n in nodes if n.time_last.date() > t]
        yield t, len(nodes)

        t += d

def normal(ports):
    for p in ports:
        n = p.port.lower()
        if 'vlan' in n or 'channel' in n:
            continue
        yield p

def get_nodes(devs):
    nodes=[]
    for ip in devs:
        d = netdisco_db.Device.find(ip)
        for p in normal(d.ports):
            if p.nodes:
                #due to mapper configuration, nodes[0] is most recent node
                nodes.append((p.nodes[0]))
    return nodes

def show_report(devs):
    nodes = get_nodes(devs)

    for node in nodes:
        print "%-15s %-19s %s %s" % (node.switch, node.port, node.time_last.strftime("%Y-%m-%d"), node.mac)

    print
    print

    print "cutoff     Number of Active Ports"
    for day, num_nodes in older_ranges(nodes):
        print day, num_nodes
    
    devices = {}
    #collect in use ports
    for node in nodes:
        devices.setdefault(node.switch,[]).append(node.port)

    print
    print "Port usage by switch:"
    for x, ports in devices.items():
        d = netdisco_db.Device.find(x)
        print x, len(ports), "out of", len(list(normal(d.ports)))
        f = open("/tmp/shutdown/%s.txt" % x,'w')
        for p in d.ports:
            if '/' not in p.port: continue
            if 'gig' in p.port.lower(): continue
            if p.port in ports: continue
            if p.status == 'disabled': continue
            if p.remote_id: continue
            if p.status == 'up':
                print p, 'is up'
                continue
            f.write("interface %s\n  shutdown\n" % p.port)
        f.close()
        

if __name__ == "__main__":
    devs = sys.argv[1:]
    show_report(devs)

