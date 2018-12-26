from ipaddress import IPv4Network, IPv4Address

from Config import Config


def get_ip_address(index, base_ip_address):
    return str(IPv4Address(int(base_ip_address) + index))


def get_port(index, base_port, vary_ports):
    return base_port + (index if vary_ports else 0)


class NetworkTopology:
    # TODO: do fancy stuff with network topology definitions
    def __init__(self, topology, config: Config):
        self.topology = topology
        self.nids: list = topology
        self.nodes = self.generate_nodes(config)

    def generate_nodes(self, config: Config):
        nodes = {
            node['nid']: {
                'image': node['program'],
                'peer_nids': set((node['connections'] if 'connections' in node else []) +
                                 ([node['nid']] if config.nodes_self_connected else [])),
                'ip_address': get_ip_address(index, config.base_ip_address),
                'port': get_port(index, config.base_port, config.vary_ports)
            }
            for index, node
            in enumerate(self.nids)
        }
        # Add nid to peer_nid list of all connected peers
        for node in nodes:
            for peer_nid in (node['connections'] if 'connections' in node else []):
                nodes[peer_nid]['peer_nids'].add(node['nid'])
        return nodes
