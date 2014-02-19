collectd-bondstatus
================
This is a python plugin for collecting NIC bond status.

It requires the python plugin in collectd in order to gather data.

The script detects and monitor all bonds. It assumes there's 2 NICs in a given bond.

It checks the number of NICs in the bond as well as the MII status of the bond itself and all NICs.

Requirements
------------
*collectd*  
collectd must have the Python plugin installed. See (<http://collectd.org/documentation/manpages/collectd-python.5.shtml>)


Example
-------
    <LoadPlugin python>
        Globals true
    </LoadPlugin>

    <Plugin python>
        # bondstatus.py is at /opt/collectd/lib/collectd/python
        ModulePath "/usr/lib64/collectd/"
        Import bondstatus
    </Plugin>


Credits
-------

In production use at [exoscale](https://www.exoscale.ch) and licensed under the MIT License.
