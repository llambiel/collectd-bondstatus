#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Loic Lambiel, exoscale
# This is a collectd python script to detect bondings status. any MII state other than "up" will be reported as failed. We expect 2 NICs with "up" status in our bond.


def get_bond():
    try:
        path = "/proc/net/bonding/"
        bondList = os.listdir(path)
        return bondList
    except Exception:
        return


def check_bond_status(strBondName):
    try:
        bondStatus = {}
        n = 0
        strBondPath = "/proc/net/bonding/%s" % strBondName
        for line in open(strBondPath).readlines():
            if "MII Status" in line:
                strState = line.split(":")
                strState = strState[1].strip()
                if strState != "up":
                    # bond nok
                    intState = 1
                    bondStatus['intState'] = intState
                    bondStatus['strState'] = strState
                    # we stop at first error
                    return bondStatus
                else:
                    # bond ok
                    n = n + 1
                    intState = 0
                    bondStatus['intState'] = intState
                    bondStatus['strState'] = strState
        # we expect to find 3 "up" in our typical bond, trigg error if not
        if n != 3:
            intState = 1
            strState = "One NIC is missing in bond"
            bondStatus['intState'] = intState
            bondStatus['strState'] = strState
        return bondStatus
    except Exception:
        return

try:
    import collectd
    import os

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
        bondList = get_bond()
        if bondList:
            for bond in bondList:
                bond_status = check_bond_status(bond)
                val = collectd.Values(plugin=NAME, type="gauge")
                if bond_status:
                    val.values = [bond_status['intState']]
                    logger('verb', "Bond %s status is: %s" % (bond, bond_status['intState']))
                    val.type_instance = "%s" % bond
                    val.type = "gauge"
                    val.dispatch()
        else:
            logger('verb', "no bond found")

    collectd.register_read(read_callback)


except ImportError:
    # we're not running inside collectd
    # it's ok
    import os

    bondList = get_bond()
    if bondList:
        for bond in bondList:
            bond_status = check_bond_status(bond)
            if bond_status:
                if bond_status['intState'] == 0:
                    print "Bond %s is up" % bond
                else:
                    print "Bond %s error:%s" % (bond, bond_status['strState'])
    else:
        print "no bond found"
