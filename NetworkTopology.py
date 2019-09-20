from ipaddress import IPv4Address

from Config import Config
from constants import DEFAULT_NID_STARTING_NUMBER, DEFAULT_NID_NUMBER_INCREMENT, DEFAULT_NID_PREFIX, DEFAULT_NID_SUFFIX

SINGLE_TYPE_NODE_GROUPS = ['line', 'bus', 'ring', 'fully_connected']


def get_ip_address(index, base_ip_address):
    return str(IPv4Address(int(base_ip_address) + index))


def get_port(index, base_port, vary_ports):
    return base_port + (index if vary_ports else 0)


def generate_line_proto_nodes(nids: list, program: str):
    return [{'nid': nid,
             'program': program,
             'connections': [nids[index + 1]]}
            for index, nid
            in enumerate(nids[:-1])] + [{'nid': nids[-1], 'program': program}]


def generate_proto_nodes(topology):
    proto_nodes: list = topology['single_nodes'].copy()
    for group in (topology['node_groups'] if 'node_groups' in topology else []):
        if group['type'] in SINGLE_TYPE_NODE_GROUPS:
            nid_starting_number: int = (group['nid_starting_number']
                                        if 'nid_starting_number' in group
                                        else DEFAULT_NID_STARTING_NUMBER)
            nid_number_increment: int = (group['nid_number_increment']
                                         if 'nid_number_increment' in group
                                         else DEFAULT_NID_NUMBER_INCREMENT)
            nid_prefix: str = group['nid_prefix'] if 'nid_prefix' in group else DEFAULT_NID_PREFIX
            nid_suffix: str = group['nid_suffix'] if 'nid_suffix' in group else DEFAULT_NID_SUFFIX
            nids: list = [f'{nid_prefix}'
                          f'{nid_starting_number + node_index * nid_number_increment}'
                          f'{nid_suffix}'
                          for node_index
                          in range(0, group['number_nodes'])]
            proto_nodes.extend(globals()[f'generate_{group["type"]}_proto_nodes'](nids, group['node_program']))
        elif group['type'] == 'star':
            pass
    return proto_nodes


def generate_nodes(config: Config, proto_nodes: list):
    nodes = {
        proto_node['nid']: {
            'image': proto_node['program'],
            'peer_nids': set((proto_node['connections'] if 'connections' in proto_node else []) +
                             ([proto_node['nid']] if config.nodes_self_connected else [])),
            'ip_address': get_ip_address(index, config.base_ip_address),
            'port': get_port(index, config.base_port, config.vary_ports)
        }
        for index, proto_node
        in enumerate(proto_nodes)
    }
    # Add nid to peer_nid list of all connected peers
    for nid, node in nodes.items():
        for peer_nid in (node['peer_nids']):
            nodes[peer_nid]['peer_nids'].add(nid)
    return nodes


class NetworkTopology:
    # TODO: do fancy stuff with network topology definitions
    def __init__(self, topology, config: Config):
        self.proto_nodes: list = generate_proto_nodes(topology)
        self.nodes = generate_nodes(config, self.proto_nodes)


