onmsNetbox
==========

A tool for importing devices from Netbox into OpenNMS.

This tool connects to Netbox using its API, queries for devices to add to
OpenNMS, collects a bunch of information for each of the devices, and finally
creates an OpenNMS requisition.xml configuration, that gets imported into
OpenNMS using its REST-API.

Installation
------------

To install, clone the repository, create a python virtualenv, and install
the python module using setuptools.

    git clone
    cd onmsNetbox
    
    python -m venv ./venv
    source venv/bin/activate
    
    python setup.py install

Finally, copy the configuration file and the template file.


Configuration
-------------

A configuration file is needed to provide login credentials for opennms, as 
well as an API token for netbox.

The tool will automatically try to load the configuration file from:

   1) /etc/onmsNetbox/config.yaml
   2) (projectDirectory)/config.yaml

Within the configuration file, please provide the following information:

    netbox:
      token:

    opnmnms:
      username:
      password:

Further, a template file is needed at the same location as the configuration file.


Usage
-----
````
Usage: onmsNetbox [OPTIONS]

Options:
  -n, --netbox TEXT       FQDN to Netbox (default: https://netbox.rz.hs-fulda.de)
  -o, --opennms TEXT      FQDN of OpenNMS (default: https://opennms.rz.hs-fulda.de)
  -r, --requisition TEXT  Name of the OpenNMS requisition (default: Netbox)
  -s, --snmp              Output MGMT IPv4 addresses of all devices to add to
                          OpenNMS SNMP configuration
  -d, --debug             Enable debug logging
  -t, --test              Only print the config, but do not add it to OpenNMS.
  --help                  Show this message and exit.
````


Monitoring SNMP-Interfaces
--------------------------

To monitor the interface status of our LAG-Interfaces, the following service
monitor is required in OpenNMS.

    <service name="SNMP-Interface" interval="30000" user-defined="false" status="on">
        <pattern><![CDATA[^SNMP-Interface-(?<iface>.*)]]></pattern>
        <parameter key="oid" value=".1.3.6.1.2.1.2.2.1.2.${pattern:iface}"/>
    </service>
    <monitor service="SNMP-Interface" class-name="org.opennms.netmgt.poller.monitors.SnmpMonitor"/>


License: MIT
------------

Copyright 2021 Sven Reissmann <sven.reissmann@rz.hs-fulda.de>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
