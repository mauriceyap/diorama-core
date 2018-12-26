PYTHON3 = 'python3'

CONTAINER_WORKING_DIRECTORY = 'container_working_directory'
CONTAINER_RUN_COMMAND = 'container_run_command'
# the program should accept the following command-line arguments:
# - comma-separated list of the nids of connected nodes ("peer" nids) e.g. alice,bob1,bob2,charlie
# - the node's own nid
# - the node's port
# - the path to the node's main function/method

RUNTIME_DATA = {
    PYTHON3: {
        CONTAINER_WORKING_DIRECTORY: '/usr/src/app',
        CONTAINER_RUN_COMMAND: ['python', '-u', 'main.py']
    }
}


def get_container_working_directory(runtime: str):
    return RUNTIME_DATA[runtime][CONTAINER_WORKING_DIRECTORY]


def get_container_run_command(runtime: str):
    return RUNTIME_DATA[runtime][CONTAINER_RUN_COMMAND]
