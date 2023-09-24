import os
import shutil
from urllib.parse import urlparse
import requests
import json
import subprocess
from queue import Queue as t_Queue

import myPath
from res.scripts.config import config, ThreadCommand, STRING

REPO_URL = "https://raw.githubusercontent.com/shinnenijou/voice-recognizer-API/main/"

PROXIES = None
if config.get_value(STRING.CONFIG_PROXY):
    PROXIES = {
        'http': config.get_value(STRING.CONFIG_PROXY),
        'https': config.get_value(STRING.CONFIG_PROXY),
    }


def parse_version(string: str):
    temp = []

    for segment in string.split('.'):
        temp.append(int(segment))

    return temp


def encode_version(version: list[int]):
    temp = []

    for i in range(len(version)):
        temp.append(str(version[i]))

    return '.'.join(temp)


def get_remote_file(remote_path:str):
    file = ''
    url = urlparse(REPO_URL + remote_path)
    try:
        response = requests.get(url.geturl(), proxies=PROXIES)
    except Exception as e:
        print(str(e))
        return file

    if response.status_code == 200:
        file = os.path.abspath(os.path.join(myPath.TEMP_PATH, remote_path))
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, 'wb') as f:
            f.write(response.content)

    return file


def get_remote_version() -> list[tuple[list[int], dict]]:
    versions = []
    file = os.path.join(myPath.TEMP_PATH, 'version.json')
    if not os.path.exists(file):
        file = get_remote_file("version.json")

    if file == '':
        return versions

    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = json.loads(f.read())
            for version, version_info in content.items():
                versions.append((parse_version(version), version_info))

            versions.sort(key=lambda x: x[0])

        os.remove(file)
    except json.JSONDecodeError:
        pass

    return versions


def update_files(files: dict, queue: t_Queue):
    complete_flag = True
    dst_map = {}

    i = 1
    size = len(files)
    for remote_file, method in files.items():
        temp_file = ''

        if method == 'A' or method == 'M':
            temp_file = get_remote_file(remote_file)

            if temp_file == '':
                complete_flag = False
                break

        dst_map[remote_file] = (method, temp_file)
        queue.put((ThreadCommand.ShowDownloadProgress, [i, size]))
        i += 1

    if complete_flag:
        for remote_file, op in dst_map.items():
            dst = os.path.abspath(os.path.join(myPath.WORK_DIR, remote_file))

            if op[0] == 'A' or op[0] == 'M':
                if not os.path.exists(dst):
                    os.makedirs(os.path.dirname(dst), exist_ok=True)

                shutil.copy(op[1], dst)
                os.remove(op[1])
            elif op[0] == 'D':
                if os.path.exists(dst):
                    os.remove(dst)

        return True

    return False


def make_temp_py(module_name: str):
    data = f"""
try:
    import {module_name}
    exit(0)
except ModuleNotFoundError:
    exit(-1)
"""
    file = os.path.join(myPath.TEMP_PATH, f'import_{module_name}.py')
    with open(file, 'w') as f:
        f.write(data)

    return file


def is_module_available(module_name: str):
    file = make_temp_py(module_name)
    subp = subprocess.run(f'{myPath.PYTHON_PATH} -s {file}', shell=True)
    os.remove(file)

    return subp.returncode == 0


def update_dependency(module, version=''):
    subp = None
    if not is_module_available(module):
        if version == '':
            subp = subprocess.run(f"{myPath.PYTHON_PATH} -s -m pip install {module}", shell=True)
        else:
            subp = subprocess.run(f"{myPath.PYTHON_PATH} -s -m pip install {module}=={version}", shell=True)

    return subp.returncode == 0


def update_dependencies(modules: dict):
    for module, version in modules.items():
        if not update_dependency(module, version):
            return False

    return True


def check_update(queue: t_Queue):
    local_version = parse_version(config['global'].get('version', '0.0.0'))
    versions = get_remote_version()
    update_flag = False

    for remote_version, version_info in versions:
        if local_version < remote_version:
            result = update_files(version_info.get('update_files', {}), queue)
            if not result:
                break

            result = update_dependencies(version_info.get('dependencies', {}))
            if not result:
                break

            local_version = remote_version
            update_flag = True

    config.set('global', 'version', encode_version(local_version))
    config.save()

    return update_flag
