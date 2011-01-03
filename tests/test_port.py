from netdisco import db
import sqlalchemy
import sys

def test_start():
    print "Testing %s" % (sys.version)
    print "on SA ver: %s" % sqlalchemy.__version__

def test_find_admin_disabled():
    #for now just make sure nothing is broken
    ports = db.Port.find_admin_disabled()
    for p in ports:
        assert p.is_disabled == True

IP = '10.1.2.2'
MAC = '00:11:22:33:44:55'
UIP = '10.1.2.100'

def test_get_by_ip():
    d = db.Device.find(IP)
    p = db.Port.get_by_ip(UIP)
    assert p.device.ip == IP

def test_get_by_mac():
    p = db.Port.get_by_mac(MAC)
    assert p.device.ip == IP

def test_find():
    p = db.Port.get_by_mac(MAC)

    assert p == db.Port.find(mac=MAC)
    assert p == db.Port.find(switch=p.device.ip,port=p.port)

def test_find_all():
    #for now just make sure nothing is broken
    ports = db.Port.find_all(mac=MAC)

def test_find_by_vlan():
    #for now just make sure nothing is broken
    ports = db.Port.find_by_vlan('666')
    for p in ports:
        assert p.vlan == '666'

def test_find_with_neighbors():
    #for now just make sure nothing is broken
    for p in db.Port.find_with_neighbors():
        print p

def test_find_non_trunking():
    #for now just make sure nothing is broken
    for p in db.Port.find_non_trunking():
        print p

def test_find_by_description():
    num=0
    for p in db.Port.find_by_description("vmware"):
        assert 'vmware' in p.name.lower()
        num+=1

    assert num==1
