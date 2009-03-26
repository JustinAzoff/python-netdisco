from netdisco import db
import sqlalchemy
import sys

def test_start():
    print "Testing %s" % (sys.version)
    print "on SA ver: %s" % sqlalchemy.__version__

IP = '10.1.2.2'
def test_device_find():
    d = db.Device.find(IP)

    assert d.ip == IP

def test_device_neighbors():
    d = db.Device.find(IP)
    for n in d.neighbors:
        print n
        assert n['remote_id'] == n['device'].name

def test_generate_descriptions():
    d = db.Device.find(IP)

    #for now just make sure nothing is broken
    for port,descr in d.generate_descriptions().items():
        print port, descr

def test_active_ips():
    d = db.Device.find(IP)

    #for now just make sure nothing is broken
    for ip in d.active_ips:
        print ip

def test_active_nodes():
    d = db.Device.find(IP)

    #for now just make sure nothing is broken
    for n in d.active_nodes:
        print n
    
def test_active_node_ips():
    d = db.Device.find(IP)

    #for now just make sure nothing is broken
    for ip in d.active_node_ips:
        print ip
    
def test_ports_as_dict():
    d = db.Device.find(IP)

    #for now just make sure nothing is broken
    for info in d.ports_as_dict:
        print info

def test_has_layer():
    d = db.Device.find(IP)

    assert d.has_layer(2)

def test_last_to_be_macsucked():
    d = db.Device.last_to_be_macsucked()

def test_find_aps():
    #for now just make sure nothing is broken
    for ap in db.Device.find_aps():
        print ap


def test_find_by_subnet():
    devs = db.Device.find_by_subnet("10.1.2.0/24")

    assert IP in [d.ip for d in devs]

