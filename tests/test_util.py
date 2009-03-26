from netdisco import db
import sqlalchemy
import sys

def test_start():
    print "Testing %s" % (sys.version)
    print "on SA ver: %s" % sqlalchemy.__version__

IP = '10.1.2.2'
MAC = '00:11:22:33:44:55'
UIP = '10.1.2.100'
DISABLED_IP = '10.1.2.101'

def test_get_macs_for_ip():
    assert MAC in db.util.get_macs_for_ip(UIP)

def test_get_ips_for_mac():
    assert UIP in db.util.get_ips_for_mac(MAC)


def test_get_all_ips():
    data = db.util.get_all_ips()
    assert IP in [ip for (ip,name) in data]

def test_get_all_ips_dict():
    data = db.util.get_all_ips_dict()

    assert IP in [x['ip'] for x in data]

def test_get_dead_links():
    #for now just make sure nothing is broken
    data = db.util.get_dead_links()

def test_find_aps():
    data = db.util.find_aps()
    for ip,name,type in data:
        assert 'AIR' in type

def test_is_disabled():
    assert db.util.is_disabled(mac=MAC) == False
    assert db.util.is_disabled(ip=DISABLED_IP) == True

def test_get_old_macs_by_subnet():
    #for now just make sure nothing is broken
    data = db.util.get_old_macs_by_subnet('10.1.2.0/24')
    print data

def test_get_wireless_macs():
    #for now just make sure nothing is broken
    data = db.util.get_wireless_macs()

def test_find_ports_with_many_macs():
    #for now just make sure nothing is broken
    data = db.util.find_ports_with_many_macs()


def test_get_vlan_counts():
    #for now just make sure nothing is broken
    data = db.util.get_vlan_counts([IP])

