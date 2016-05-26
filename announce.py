#!/usr/bin/env python

from __future__ import print_function

from lib.consul import Consul
from lib.docker import Docker

import argparse
import signal
import sys
import time
import os

parser = argparse.ArgumentParser(description='Register the docker containers using a specific network as nodes in '
                                             'Consul.')
parser.add_argument('--daemon', '-d', action='store_true', help='Make it run in background', default=False)
parser.add_argument('--interval', '-i', type=int, help='The interval in seconds between two checks', default=60)
# Consul options
parser.add_argument('--consul', dest='consul_host', help='Consul host address',
                    default=os.environ.get('CONSUL_HOST', None))
parser.add_argument('--consul-port', help='Consul port', default=os.environ.get('CONSUL_PORT', 8500))
parser.add_argument('--consul-scheme', help='Consul port', default=os.environ.get('CONSUL_SCHEME', 'http'))
# Docker options
parser.add_argument('--network', dest='network_name', default=os.environ.get('NETWORK', None),
                    help='The name of the network containing the docker containers')
parser.add_argument('--docker', dest='docker_url', help='Docker Engine URL',
                    default=os.environ.get('DOCKER_HOST', None))

args = parser.parse_args()

if not args.network_name:
    sys.stderr.write("You must specify the network name.")
    parser.print_help()
    sys.exit(1)

if not args.docker_url:
    sys.stderr.write("You must specify the Docker Engine URL.")
    parser.print_help()
    sys.exit(1)

if not args.consul_host:
    sys.stderr.write("You must specify the Consul host address.")
    parser.print_help()
    sys.exit(1)

consul = Consul(args.consul_host, args.consul_port, args.consul_scheme)
docker = Docker(args.docker_url)


def loop():
    containers = docker.get_containers_in_networks(docker.get_multinodes_networks(args.network_name))
    registered_services = consul.get_nodes_for_services_with_tag(args.network_name)

    added_services = []
    for container_id in containers:
        if container_id not in registered_services:
            container_data = docker.inspect_container(container_id)
            name = container_data['Name'][1:]
            consul.register_service(
                id=container_id,
                name=name,
                node=name,
                address=container_data['NetworkSettings']['Networks'][args.network_name]['IPAddress'],
                tags=[args.network_name]
            )
            added_services.append((name, container_id))

    if added_services:
        print('Services registered:')
        for service in added_services:
            print("- {0} ({1})".format(service[0], service[1]))

    removed_services = []
    for service in registered_services:
        if service not in containers:
            node = registered_services[service]['Node']
            consul.deregister_service(node, service)
            print("- {0} ({1})".format(node, service))

    if removed_services:
        print('Services removed:')
        for service in removed_services:
            print("- {0} ({1})".format(service[0], service[1]))


if not args.daemon:
    print("Updating the service and node lists...")
    loop()
    print("Done.")
    sys.exit(0)

is_running = True


def signal_handler(signal, frame):
    global is_running
    print("Shutting down the announcer...")
    is_running = False
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

print("Starting the announcer as a daemon...")
while is_running:
    loop()
    time.sleep(args.interval)
