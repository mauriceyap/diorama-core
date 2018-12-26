import argparse
import errno
import sys

import yaml
import docker
from docker.errors import APIError as dockerAPIError
from docker.types import IPAMConfig, IPAMPool

import constants
from Config import Config
from NetworkTopology import NetworkTopology
from Programs import Programs
import runtimes


DOCKER_CLIENT = docker.from_env()
DOCKER_API_CLIENT = docker.APIClient()


def exit_suggest_force_clean_running_containers():
    sys.stderr.write("There are nodes that haven't been removed because they are still running. "
                     "Stop them first, or run a force clean\n")
    sys.exit(errno.EACCES)


def clean(nids, image_names, force):
    try:
        for nid in nids:
            DOCKER_CLIENT.containers.get(nid).remove(force=force)
    except dockerAPIError as e:
        if e.status_code == 404:
            pass
        elif e.status_code == 409:
            exit_suggest_force_clean_running_containers()

    try:
        for image_name in image_names:
            DOCKER_CLIENT.images.remove(image=image_name, force=force, noprune=False)
        DOCKER_CLIENT.networks.get(constants.NETWORK_NAME).remove()
    except dockerAPIError:
        pass


def create_network(config: Config):
    DOCKER_CLIENT.networks.prune()
    DOCKER_CLIENT.networks.create(
        name=constants.NETWORK_NAME,
        driver='bridge',
        ipam=IPAMConfig(pool_configs=[IPAMPool(subnet=str(config.network_subnet))]),
        internal=True
    )


def create_containers(nodes, programs):
    for nid, node in nodes.items():
        program = programs[node['image']]
        peer_nid_list = ','.join(node['peer_nids'])
        DOCKER_API_CLIENT.create_container(
            node['image'],
            name=nid,
            command=runtimes.get_container_run_command(program['runtime']) + [peer_nid_list, nid, str(node['port']),
                                                                              program['node_main_path']],
            detach=True,
            working_dir=runtimes.get_container_working_directory(program['runtime']),
            ports=[(node['port'], 'udp')]
        )
        DOCKER_CLIENT.networks.get(constants.NETWORK_NAME).connect(nid, ipv4_address=node['ip_address'])


def start_containers(nodes: dict):
    for nid in nodes.keys():
        DOCKER_CLIENT.containers.get(nid).start()


def main(args):
    config: Config = Config()
    config.import_config(yaml.load(open('user_configuration/diorama_custom_config.yml', 'r')))
    network_topology = NetworkTopology(yaml.load(open('user_configuration/diorama_network.yml', 'r')), config)
    programs = Programs(yaml.load(open('user_configuration/diorama_programs.yml', 'r')))

    if args.clean:
        clean([node['nid'] for node in network_topology.nids],
              [program['program_name'] for program in programs.programs_list],
              args.force)
    else:
        create_network(config)
        programs.build_docker_images(DOCKER_CLIENT, network_topology.nodes)
        create_containers(network_topology.nodes, programs)
        start_containers(network_topology.nodes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--clean', '-c', action='store_true', help='remove built artifacts')
    parser.add_argument('--force', '-f', action='store_true', help='force remove built artifacts')
    main(parser.parse_args())


