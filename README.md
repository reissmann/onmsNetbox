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
   2) <workingDirectory>/config.yaml

Within the configuration file, please provide the following information:

    netbox:
      token:

    opnmnms:
      username:
      password:


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
