## User configuration files

This directory will be populated with three YAML files:

### `diorama_custom_config.yml`
Some number of (including zero) key-value pairs of custom advanced settings. Examples include:

```yaml
base_ip_address: '181.30.0.2'
network_subnet: '181.30.0.0/16'
nodes_self_connected: False
```
*Vanilla settings:*
```yaml
{}
```
A complete list of possible settings and their default values can be found in `Config.py`.

### `diorama_network.yml`
A list of nodes with attributes:
- `nid` *the node ID*
- `program` *the program which this node should run*
- `connections` *a list of the `nid`s of all nodes which this node is connected to*

### `diorama_programs.yml`
A list of programs with attributes:
- `program_name` *name of the program*
- `node_main_path` *path to the 'main' method/function for the node*
- `runtime` *e.g. python3, nodejs8, ruby2, scala2-12*