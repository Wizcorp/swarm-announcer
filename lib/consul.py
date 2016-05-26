from __future__ import absolute_import
import six

import consul


class Consul:
    def __init__(self, host, port, scheme):
        self._c = consul.Consul(host=host, port=port, scheme=scheme)

    def register_service(self, id, name, node, address, tags=None):
        return self._c.catalog.register(
            node=node,
            address=address,
            service={
                'ID': id,
                'Service': name,
                'Tags': tags,
                'Address': address
            }
        )

    def deregister_service(self, node, service_id):
        return self._c.catalog.deregister(
            node=node,
            service_id=service_id
        )

    def get_nodes_for_services_with_tag(self, tag):
        services = self._c.catalog.services()[1]
        matching_services = [self._c.catalog.service(service) for (service, tags) in six.iteritems(services) if
                             tag in tags]
        nodes = {}
        for service in matching_services:
            if not service or not service[1] or not service[1][0]:
                continue
            service_definition = service[1][0]
            if "ServiceID" not in service_definition:
                continue
            nodes[service_definition["ServiceID"]] = service_definition
        return nodes
