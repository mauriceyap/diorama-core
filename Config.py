from ipaddress import IPv4Address, IPv4Network

LOWERCASE_STRINGS_FOR_TRUE = ['true', 't', 'yes', 'y']

convert_from_string_functions = {
    'base_ip_address': lambda s: IPv4Address(s),
    'network_subnet': lambda s: IPv4Network(s),
    'port': lambda s: int(s),
    'nodes_self_connected': lambda s: s.lower() in LOWERCASE_STRINGS_FOR_TRUE,
    'vary_ports': lambda s: s.lower() in LOWERCASE_STRINGS_FOR_TRUE
}


class Config:
    def __init__(self):
        self.base_ip_address: IPv4Address = IPv4Address('172.190.0.4')
        self.network_subnet: IPv4Network = IPv4Network('172.190.0.0/16')
        self.base_port: int = 2000
        self.nodes_self_connected: bool = True
        self.vary_ports: bool = True

    def import_config(self, new_config: dict):
        for name, value in new_config.items():
            self.__setattr__(name, (convert_from_string_functions[name](value)
                                    if name in convert_from_string_functions
                                    else value))
