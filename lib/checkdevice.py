#!/usr/bin/env python2.4
from netdisco.db import *
import fping
from sets import Set as set
from pinginventory import PingInventory

class NotFound(Exception):
    pass
class DeviceNotFound(NotFound):
    pass

def check(switch=None,ip=None,mac=None):
    """check for pingable devices on "switch" or find "ip" or "mac" and check that device"""
    if switch:
        dev = Device.find(ip=switch)
        if not dev:
            raise DeviceNotFound, "Device %s not found" % switch
    elif ip:
        port = Port.get_by_ip(ip)
        if not port:
            raise NotFound, "ip %s not found" % ip
        dev = port.device
    elif mac:
        port = Port.get_by_mac(mac)
        if not port:
            raise NotFound, "mac %s not found" % mac
        dev = port.device
    
    return check_switch(device=dev)

def check_switch(device):
    """Helper function that does the actual checking"""
    p = PingInventory(c.get("ping_inventory","ini_file"))
    inventory = set([x.ip for x in p.latest().nodes])
    ips = set( device.active_node_ips )
    remove = set()
    for ip in ips:
        if ip not in inventory:
            remove.add(ip)
    
    ips = ips - remove
    up = set(fping.pingmany(ips,fast=True))
    down = ips - up
        
    return up, down

def simplecheck(switch=None,ip=None,mac=None):
    up, down = check(switch, ip, mac)
    return len(up) > 0

def check_switch_counts(ip):
    up, down = check(switch=ip)
    return len(up), len(down)

def main():
    import sys
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-s", "--switch", dest="switch", action="store", help="Check this switch", default=None)
    parser.add_option("-i", "--ip", dest="ip", action="store", help="Check the switch this ip is on", default=None)
    parser.add_option("-m", "--mac", dest="mac", action="store", help="Check the switch this mac is on", default=None)

    (options, args) = parser.parse_args()
    if not(options.switch or options.ip or options.mac):
        parser.print_help()
        sys.exit(1)

    up, down=check(switch=options.switch, ip=options.ip, mac=options.mac)
    print len(up), "devices up", ' '.join(list(up))
    print
    print len(down), "devices down", ' '.join(list(down))

    ok = len(up) >= len(down)
    if not ok:
        print "More devices down than up, might be bad"
