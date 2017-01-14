#!/usr/bin/env python2.7
from __future__ import print_function
import argparse
import ConfigParser
import libcloud
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import os
import sys

# Setup argparse
# common options to all commands
common_options = argparse.ArgumentParser(add_help=False)
# common_options.add_argument('-c', '--config',
#                            metavar='FILE',
#                            dest='config',
#                            default=None,
#                            help='Config file (~/.dorc by default)')
common_options.add_argument('-a', '--api-key',
                            metavar='KEY',
                            dest='api',
                            default=None,
                            help='api key to use with digital ocean')
common_options.add_argument('-s', '--ssh-key',
                            metavar='KEY',
                            dest='ssh',
                            default=None,
                            help='public key to use for the droplet')
common_options.add_argument('-l', '--list',
                            action='store_true',
                            help=('list IDs for disk size, image type, '
                                  'and datacenter location'))
server_uuid = argparse.ArgumentParser(add_help=False)
server_uuid.add_argument('-i', '--id',
                         required=True,
                         dest='uuid')

# create main and subparser
parser = argparse.ArgumentParser(
    parents=[common_options],
    description='simple script to interact with droplets')
subparser = parser.add_subparsers(dest='action', help='available actions')

# parsers for actions
# list parser
parser_list = subparser.add_parser('list',
                                   help=('list IDs for disk size, image '
                                         'type, and datacenter location'))
# create parser
parser_create = subparser.add_parser('create',
                                     help='create a new droplet')
parser_create.add_argument('-d', '--datacenter',
                           required=True,
                           type=int,
                           help='datacenter id (from list command)')
parser_create.add_argument('-n', '--size',
                           required=True,
                           type=int,
                           help='VM Size id (from list command)')
parser_create.add_argument('-i', '--image',
                           required=True,
                           type=int,
                           help='Image ID (from list command)')
parser_create.add_argument('hostname', help='name of VM')
# destroy parser
parser_destroy = subparser.add_parser('destroy',
                                      parents=[server_uuid],
                                      help='destroy a droplet')
# list_node parser
parser_list_nodes = subparser.add_parser('listnodes', help='List all nodes')


# Functions
def init_driver(token):
    """Initializes a driver for digital ocean"""
    cls = get_driver(Provider.DIGITAL_OCEAN)
    return cls(token, api_version='v2')


def list_attributes(token):
    """List VM sizes, images, and datacenter locations"""
    driver = init_driver(token)

    sizes = driver.list_sizes()
    print("VM Sizes:")
    for id, size in zip(range(len(sizes)), sizes):
        print("\t{0:2}: {1}".format(id, size.name))

    images = driver.list_images()
    print("Images:")
    for id, image in zip(range(len(images)), images):
        print("\t{0:2}: {1} {2}".format(id,
                                        image.extra.get(
                                            'distribution',
                                            '\b\b'),
                                        image.name))

    locations = driver.list_locations()
    print("Datacenter locations:")
    for id, location in zip(range(len(locations)), locations):
        print("\t{0:2}: {1}".format(id, location.name))


def create_machine(token, datacenter, size, image, hostname, ssh_key):
    """Create a machine"""
    if hostname is None:
        print("You must provide a hostname")
        sys.exit(3)
    driver = init_driver(token)
    key = None

    lsize = driver.list_sizes()[size]
    limage = driver.list_images()[image]
    ldatacenter = driver.list_locations()[datacenter]
    try:
        key = driver.create_key_pair('do default key', ssh_key)
    except libcloud.common.exceptions.BaseHTTPError:
        key = driver.get_key_pair('do default key')

    options = {
        'ssh_keys': [key.fingerprint]
    }
    node = driver.create_node(hostname,
                              lsize,
                              limage,
                              ldatacenter,
                              ex_create_attr=options)
    print("{}".format(node.get_uuid()))


def destroy_machine(token, uuid):
    """Destroy a machine by its given uuid"""
    driver = init_driver(token)

    try:
        node = [n for n in driver.list_nodes() if n.get_uuid() == uuid][0]
    except IndexError:
        print("ID not found!")
        sys.exit(4)
    node.destroy()


def list_nodes(token):
    """List all nodes attached to an account"""
    driver = init_driver(token)

    print("Nodes:")
    for node in driver.list_nodes():
        print("{} ({}) @ ({}): {}".format(node.name,
                                          node.state,
                                          ','.join(node.public_ips),
                                          node.get_uuid()))


def main(args=None):
    """Entry point for the dont script"""
    if args is None:
        args = sys.argv[1:]

    # local variables
    api_key = None
    ssh_key = None
    config_file = os.path.expanduser('~/.dorc')

    parsed = parser.parse_args()

    # we need at least the api key to start
    if parsed.api is None:
        config = ConfigParser.SafeConfigParser()
        if not os.path.isfile(config_file):
            print("API key not set. Please specify with -a or in ~/.dorc")
            sys.exit(1)
        try:
            config.read(config_file)
            api_key = config.get('keys', 'api')
            if parsed.ssh is None:
                ssh_key = config.get('keys', 'ssh')
        except ConfigParser.NoSectionError as e:
            print(e)
            print("Couldn't read config file")
            sys.exit(2)
        except ConfigParser.NoOptionError as e:
            print(e)
            print("Couldn't read config file")
            sys.exit(2)
    else:
        api_key = parsed.api
        ssh_key = parsed.ssh

    if parsed.action == 'list':
        list_attributes(api_key)
    if parsed.action == 'create':
        create_machine(api_key,
                       parsed.datacenter,
                       parsed.size,
                       parsed.image,
                       parsed.hostname,
                       ssh_key)
    if parsed.action == 'listnodes':
        list_nodes(api_key)
    if parsed.action == 'destroy':
        destroy_machine(api_key, parsed.uuid)

if __name__ == '__main__':
    main()
