import os
import shutil

import yaml

import constants


def generate_nid_mappings_file(nodes_with_info: dict):
    mappings_list = [{'nid': nid, 'ip_address': info['ip_address'], 'port': info['port']}
                     for nid, info
                     in nodes_with_info.items()]
    with open(constants.NID_MAPPINGS_FILE_PATH, 'w') as nid_mappings_file:
        yaml.dump(mappings_list, nid_mappings_file, default_flow_style=False)


class Programs:
    def __init__(self, programs_list: list):
        self.programs_list: list = programs_list
        self.programs_dict: dict = {program['program_name']: {p: program[p] for p in program if p != 'program_name'}
                                    for program
                                    in programs_list}

    def __getitem__(self, item: str):
        return self.programs_dict[item]

    def build_docker_images(self, docker_client, nodes):
        generate_nid_mappings_file(nodes)
        for program_name, program in self.programs_dict.items():
            shutil.copytree(os.path.join(constants.BASE_NODE_FILES_DIRECTORY, program['runtime']),
                            constants.TEMP_GENERATED_FILES_DIRECTORY)
            shutil.copy2(constants.NID_MAPPINGS_FILE_PATH, constants.TEMP_GENERATED_FILES_DIRECTORY)
            shutil.copytree(os.path.join(constants.USER_NODE_FILES_DIRECTORY, program_name),
                            os.path.join(constants.TEMP_GENERATED_FILES_DIRECTORY,
                                         constants.USER_NODE_FILES_GENERATED_SUBDIRECTORY))
            docker_client.images.build(path=constants.TEMP_GENERATED_FILES_DIRECTORY, tag=program_name, rm=True)
            shutil.rmtree(constants.TEMP_GENERATED_FILES_DIRECTORY)
        os.remove(constants.NID_MAPPINGS_FILE_PATH)
