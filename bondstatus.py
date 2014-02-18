#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Loic Lambiel, exoscale
#This is a collectd python script to detect bondings status. any MII state other than "up" will be reported as failed. We expect 2 NICs with "up" status in our bond.



def check_bond_status(intBondID):
    try:
        Bondstatus = {}
        n = 0
        strBondPath = "/proc/net/bonding/bond%d" % intBondID
        for line in open(strBondPath).readlines():
            if "MII Status" in line:
                strState = line.split(":")
                strState = strState[1].strip()
                if strState != "up":
                    #bond nok
                    intState = 1
                    Bondstatus['intState'] = intState
                    Bondstatus['strState'] = strState
                    #we stop at first error
                    return Bondstatus
                else:
                    #bond ok
                    n = n + 1
                    intState = 0
                    Bondstatus['intState'] = intState
                    Bondstatus['strState'] = strState
        #we expect to find 3 "up" in our typical bond, trigg error if not            
        if n != 3:
            intState = 1
            strState = "One NIC is missing in bond"
            Bondstatus['intState'] = intState
            Bondstatus['strState'] = strState
        return Bondstatus
    except:
        return

try:
    import collectd

    VERBOSE_LOGGING = False

    NAME = "Bondstatus"

    # logging function
    def logger(t, msg):
        if t == 'err':
            collectd.error('%s: %s' % (NAME, msg))
        elif t == 'warn':
            collectd.warning('%s: %s' % (NAME, msg))
        elif t == 'verb':
            if VERBOSE_LOGGING:
                collectd.info('%s: %s' % (NAME, msg))
        else:
            collectd.notice('%s: %s' % (NAME, msg))
   

    def read_callback():
        i = 0
        for i in range(0, 10):
            bond_status = check_bond_status(i)
            val = collectd.Values(plugin=NAME, type="gauge")
            if bond_status:
                val.values = [bond_status['intState'] ]
                logger('verb', "Bond%s status is: %s" % (i,bond_status['intState']))
                val.type_instance = "Bond%s" % i
                val.type = "gauge"
                val.dispatch()

    collectd.register_read(read_callback) 


except ImportError:
    ## we're not running inside collectd
    ## it's ok

    i = 0
    for i in range(0, 10):
        try:
            bond_status = check_bond_status(i)
            if bond_status['intState'] == 0:
                print "bond%d is up" % i
            else:
                print "bond%d error:%s" % (i,bond_status['strState'])
        except:
            continue
