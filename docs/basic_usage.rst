Basic Usage
===========

Importing
---------

    >>> import netdisco
    >>> # or
    >>> from netdisco import db as netdisco_db


Inspecting a Device
-------------------

    >>> d = netdisco.db.Device.find("10.1.2.2")
    >>> print d
    [10.1.2.2 DeviceHostname]
    >>> print d.vendor, d.model, d.serial
    cisco 356048TS CATXXXXXXXX


Inspecting a Port
-----------------
The 'ports' attribute on a Device will return the list of Port objects::

    >>> len(d.ports)
    54
    >>> for p in d.ports[-8:]: print p, p.status
    ... 
    [10.1.2.2 FastEthernet0/45] down
    [10.1.2.2 FastEthernet0/46] down
    [10.1.2.2 FastEthernet0/47] down
    [10.1.2.2 FastEthernet0/48] down
    [10.1.2.2 GigabitEthernet0/1] up
    [10.1.2.2 GigabitEthernet0/2] up
    [10.1.2.2 GigabitEthernet0/3] up
    [10.1.2.2 GigabitEthernet0/4] down
    
    >>> p = d.ports[1]
    >>> print p.speed, p.status, p.vlan
    100 Mbps up 2


Inspecting nodes
----------------
The 'nodes' attribute on Port will return the list of Node object::

    >>> for n in p.nodes: 
    ...     print n.mac, n.time_first, n.time_last
    ... 
    00:0f:fe:16:9f:7e 2008-10-28 17:23:38.992662 2009-03-26 10:41:31
    00:b0:d0:c8:36:cc 2007-04-25 10:45:02.284588 2008-10-28 15:30:54

