#!/usr/bin/env python

"""
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
"""

import os.path
import logging
import click
import pynetbox
import requests
import yamlreader as yamlreader
from jinja2 import Template


def get_config(netbox, opennms, requisition, snmp, debug, test):
    """ Try to load the configuration file, merge it with cli parameters
        and return the complete config as an array.

        @params: all cli parameters
        @return: the configuration as an array
    """
    if os.path.isfile('/etc/onmsNetbox/config.yaml'):
        filename = '/etc/onmsNetbox/config.yaml'
    elif os.path.isfile('../config/config.yaml'):
        filename = '../config/config.yaml'
    else:
        logging.error('Configuration file does not exist.')
        exit(1)

    config = yamlreader.yaml_load(filename, {"loglevel": "error"})

    if netbox and netbox != '':
        config['netbox']['fqdn'] = netbox

    if opennms and opennms != '':
        config['opennms']['fqdn'] = opennms

    if requisition and requisition != '':
        config['opennms']['requisition'] = requisition

    config['snmp'] = snmp
    config['debug'] = debug
    config['test'] = test

    return config


def get_template():
    """ Load the requisition template file.

        @return: The jinja2 template object
    """
    if os.path.isfile('/etc/onmsNetbox/requisition.xml'):
        filename = '/etc/onmsNetbox/requisition.xml'
    elif os.path.isfile('../templates/requisition.xml'):
        filename = '../templates/requisition.xml'
    else:
        logging.error('Template file does not exist.')
        exit(1)

    with open(filename) as _:
        return Template(_.read(), trim_blocks=True, lstrip_blocks=True)


def get_site(nb, siteid):
    """ For a given device, return site-specific information as a tuple.

        @param nb: pynetbox api object
        @param siteid: the ID of a site in netbox
        @return: name and coordinates (latitude and longitude) of the site
    """
    site = nb.dcim.sites.get(id=siteid)

    return site.latitude, site.longitude, site.name


def get_interface_ids(nb, name):
    """ For a given device, return an array of all SNMP-Interface-IDs that
        match the tag 'uplink'.
        Note: By our own definition, the SNMP-Interface-ID of an interface
        is set as the interface label in netbox.

        @param nb: pynetbox api object
        @param name: The name of a device in netbox
        @return: An array of all SNMP-Interface-IDs
    """
    snmp_if_ids = []
    for interface in nb.dcim.interfaces.filter(device=name, tag='uplink'):
        snmp_if_ids.append(interface.label)

    return snmp_if_ids


def opennms_import(config, output, requisition):
    """ Import the requisition configuration into OpenNMS.

        @param config: The OpenNMS config (fqdn, username, password)
        @param output: The generated requisition configuration
        @param requisition: The name of the OpenNMS requisition
    """
    headers = {'Content-Type': 'application/xml', 'Accept': 'application/xml'}

    requests.post(config['opennms']['fqdn'] + '/opennms/rest/requisitions',
                  headers=headers, data=output.encode('utf-8'),
                  auth=(config['opennms']['username'], config['opennms']['password']))

    requests.put(config['opennms']['fqdn'] + '/opennms/rest/requisitions/' + requisition + '/import',
                 auth=(config['opennms']['username'], config['opennms']['password']))


def render_requisition(config, nodelist, requisition):
    """ Render the OpenNMS requisition configuration and print or import it.
    """
    output = get_template().render(nodelist=nodelist, requisition=requisition)

    if config['test']:
        print(output)
    else:
        opennms_import(config, output, requisition)


@click.command()
@click.option('-n', '--netbox', help='FQDN for Netbox (overwrites config file value)')
@click.option('-o', '--opennms', help='FQDN for OpenNMS (overwrites config file value)')
@click.option('-r', '--requisition', help='Name of the OpenNMS requisition (overwrites config file value)')
@click.option('-s', '--snmp', default=False, is_flag=True,
              help='Output MGMT IPv4 addresses of all devices to add to OpenNMS SNMP configuration')
@click.option('-d', '--debug', default=False, is_flag=True,
              help='Enable debug logging')
@click.option('-t', '--test', default=False, is_flag=True,
              help='Only print the config, but do not add it to OpenNMS.')
def main(netbox, opennms, requisition, snmp, debug, test):
    """ onmsNetbox - Provision OpenNMS from Netbox.
    """

    # Open the config file and merge cli options
    #
    config = get_config(netbox, opennms, requisition, snmp, debug, test)

    # Configure logging
    #
    if config['debug']:
        import http.client as http_client
        http_client.HTTPConnection.debuglevel = 1
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(message)s')

    # Get netbox api object
    #
    nb = pynetbox.api(config['netbox']['fqdn'], config['netbox']['token'])

    # Get all devices that we want in OpenNMS from Netbox
    #
    devices = nb.dcim.devices.filter(tag='opennms', status='active')

    # Only print OpenNMS SNMP config lines
    #
    if config['snmp']:
        for device in devices:
            print('<specific>' + str(device.primary_ip4).split('/')[0] + '</specific>')
        exit(0)

    # Create the OpenNMS requisition
    #
    else:
        nodelist = []

        for device in devices:
            node = {
                'id': device.id,
                'name': device.name,
                'primary_ip4': str(device.primary_ip4).split('/')[0] if device.primary_ip4 is not None else None,
                'primary_ip6': str(device.primary_ip6).split('/')[0] if device.primary_ip6 is not None else None,
                'uplinks':  get_interface_ids(nb, device.name),
                'device_type': device.device_type.manufacturer.slug,
                'device_role': device.device_role.slug,
                'serial_number': device.serial,
                'asset_number': device.asset_tag
            }
            node['latitude'], node['longitude'], node['building'] = get_site(nb, device.site.id)

            nodelist.append(node)

        render_requisition(config=config, nodelist=nodelist, requisition=config['opennms']['requisition'])


if __name__ == '__main__':
    main()
