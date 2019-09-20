import yaml
import json

from Config import Config
from NetworkTopology import NetworkTopology

config: Config = Config()
config.import_config(yaml.load(open('user_configuration/diorama_custom_config.yml', 'r')))
network_topology = NetworkTopology(yaml.load(open('user_configuration/diorama_network.yml', 'r')), config)
nodes = network_topology.nodes
for nid in nodes.keys():
    nodes[nid]['peer_nids'] = list(nodes[nid]['peer_nids'])
print(json.dumps(nodes, indent=4))
