from __future__ import absolute_import

from docker import Client


class Docker:
    def __init__(self, url):
        self._cli = Client(
            base_url=url,
            version='auto'
        )

    def get_multinodes_networks(self, network_name):
        networks = [
            network for network in self._cli.networks()
            if network['Name'].endswith('/' + network_name)
            ]
        return networks

    @staticmethod
    def get_containers_in_networks(networks):
        containers = {}
        for network in networks:
            containers.update(network['Containers'])
        return containers

    def inspect_container(self, container):
        return self._cli.inspect_container(container)
