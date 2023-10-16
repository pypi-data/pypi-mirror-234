import os
import socket
import json
import netifaces

file_encoding = 'utf-8'

def check_workspace_exist(current_path):
    if current_path == os.path.dirname(current_path):
        return "", False
    for file_name in os.listdir(current_path):
        if ".ndtc" == file_name:
            return current_path, True
    return check_workspace_exist(os.path.dirname(current_path))


def check_subdirectory_workspace_exist(current_path, index=0):
    for file_name in os.listdir(current_path):
        if ".ndtc" == file_name and index >= 1:
            return os.path.join(current_path, file_name), True
    for file_name in os.listdir(current_path):
        if os.path.isdir(os.path.join(current_path, file_name)):
            index = index + 1
            subdirectory_workspace, result = check_subdirectory_workspace_exist(os.path.join(current_path, file_name),
                                                                                index)
            if result:
                return subdirectory_workspace, result
    return "", False


def check_local_workspace():
    if not os.path.exists(os.path.expanduser(os.path.join("~", '.ndtcrc'))):
        os.mkdir(os.path.expanduser(os.path.join("~", '.ndtcrc')))


def get_ip_address():
    hostname = socket.gethostname()
    return hostname


def get_config():
    dir_path = os.path.join("/", 'etc', 'ndtc')
    path = os.path.join(dir_path, 'skyeye.json')
    if not os.path.exists(path):
        config = {
            "log_path": ["/opt/log"],
            "vin": get_ip_address()
        }
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        with open(path, 'w', encoding=file_encoding) as f:
            f.write(json.dumps(config, indent=4))
        return config
    with open(path, 'r', encoding=file_encoding) as f:
        config = json.loads(f.read())
    return config
