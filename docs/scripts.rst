Standalone scripts
==================

netdisco-suck-check
-------------------
This script is designed to be run by Nagios or MON.  It will exit with an
error if the netdisco database is not being updated::

    % netdisco-suck-check
    ok: 179 | seconds=179[s]
    % echo $?
    0



netdisco-suck-report
--------------------
This script prints out a report of how long ago all your devices have been
polled::

    % netdisco-suck-report
    Oldest device: 192.168.1.1 blah_switch
    last polled at: 2009-04-01 09:11:52 (64 minutes)
    29    Devices sucked in under 1 minutes
    82    Devices sucked in under 10 minutes
    261   Devices sucked in under 20 minutes
    401   Devices sucked in under 30 minutes
    540   Devices sucked in under 40 minutes
    727   Devices sucked in under 50 minutes
    805   Devices sucked in under 60 minutes
    806   Devices sucked in under 65 minutes
    Average time = 30 minutes


netdisco-get-port
-----------------
This script prints the device and port that an IP or MAC address was last seen on::

    % netdisco-get-port 192.168.1.2
    192.168.1.1 FastEthernet0/2

    % netdisco-get-port 00:11:22:33:44:55
    192.168.1.1 FastEthernet0/2

  


netdisco-add
------------
This script queues a discover job for a device::

    % netdisco-add 192.168.1.1     

netdisco-refresh
----------------
This script queues the following jobs for a device:
 * macsuck
 * arpnip
 * refresh

::

    % netdisco-refresh 192.168.1.1     


netdisco-wait-for-jobs
----------------------
This script waits for any outstanding jobs to finish::

    % netdisco-wait-for-jobs 
    0 total jobs

    % netdisco-refresh 192.168.1.1     
    % netdisco-wait-for-jobs 
    3 total jobs
    1/3 192.168.1.1 blah_switch macsuck None
    queued
    running
    running
    done

    2/3 192.168.1.1 blah_switch arpnip None
    running
    done

    3/3 192.168.1.1 blah_switch refresh None
    done




netdisco-check-device
---------------------
TODO
