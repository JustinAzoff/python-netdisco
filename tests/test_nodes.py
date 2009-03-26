from netdisco import db
import sqlalchemy
import sys

def test_start():
    print "Testing %s" % (sys.version)
    print "on SA ver: %s" % sqlalchemy.__version__


IP = '10.1.2.2'
MAC = '0003.bacd.b521'


def test_active_nodes():
    #for now just make sure nothing is broken
    ips = db.Node_IP.get_active_ips()
    assert len(ips) > 1
