import os
import myPath
import subprocess
import json

IGNORE_FILES = [
    '.gitattributes',
    '.gitignore',
    'make_version.py',
    'README.md',
    'version.json',
    'starter.py',
    'compile.bat',
    'starter.py',
    'make-wizard.nsi',
    'icon.ico'
]

# 更新工作流: 在主分支需要更新的版本打上tag以后更新到这里, 生成version.json后提交即可
LATEST_TAG = '0.4.1'
UPDATE_ALL = False


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


def parse_git_log(text: str):
    logs = []
    start = text.find('commit')
    while start != -1:
        end = text.find('Author', start)
        commit = text[start + len('commit'): end].strip()
        logs.append(commit)
        start = text.find('commit', end)

    return logs


def parse_git_commit(test: str):
    temp = []
    for line in test.split('\n'):
        if not line.startswith(':'):
            continue

        segments = line.split()
        for i in range(len(segments)):
            if segments[i][0] not in ('A', 'M', 'D', 'C', 'R'):
                continue

            if segments[i][0] == 'A' or segments[i][0] == 'M' or segments[i][0] == 'D':
                temp.append(segments[i:])
            elif segments[i][0] == 'R':
                temp.append(['D', segments[i + 1]])
                temp.append(['A', segments[i + 2]])
            elif segments[i][0] == 'C':
                temp.append(['A', segments[i + 2]])

    return temp


def get_current_branch():
    subp = subprocess.run('git branch', shell=True, stdout=subprocess.PIPE)
    output = subp.stdout.decode('utf-8')
    for line in output.split('\n'):
        segments = line.split()
        if segments[0] == '*':
            return segments[1]

    return 'main'


def get_diff(from_tag, to_tag):
    subp = subprocess.run(f'git log --stat {from_tag}..{to_tag}', shell=True, stdout=subprocess.PIPE)
    output = subp.stdout.decode(encoding='utf-8')
    commits = parse_git_log(output)

    gross_diff = {}
    for i in range(len(commits) - 1, -1, -1):
        subp = subprocess.run(f'git show --raw {commits[i]}', shell=True, stdout=subprocess.PIPE)
        output = subp.stdout.decode(encoding='utf-8')
        diff = parse_git_commit(output)
        for (method, file) in diff:
            if os.path.basename(file) not in IGNORE_FILES:
                gross_diff[file] = method

    return gross_diff


def get_full_tree():
    temp = {}

    subp = subprocess.run('git ls-tree --full-tree -r HEAD', shell=True, stdout=subprocess.PIPE)
    output = subp.stdout.decode('utf-8')
    for line in output.split('\n'):
        segments = line.split()
        if len(segments) > 0 and os.path.basename(segments[-1]) not in IGNORE_FILES:
            temp[segments[-1]] = 'A'

    return temp


def main():
    cur_branch = get_current_branch()
    subprocess.run('git checkout main', shell=True, stdout=subprocess.PIPE)

    if not os.path.exists(os.path.abspath(os.path.join(myPath.WORK_DIR, 'version.json'))):
        with open(os.path.abspath(os.path.join(myPath.WORK_DIR, 'version.json')), 'w') as file:
            file.write('{}')

    versions = []
    with open(os.path.abspath(os.path.join(myPath.WORK_DIR, 'version.json')), 'r') as file:
        temp = json.loads(file.read())
        for version_str, version_info in temp.items():
            versions.append((parse_version(version_str), version_info))

        versions.sort(key=lambda x: x[0])

    last_version = [0, 0, 0]
    if len(versions) > 0:
        (last_version, _) = versions[-1]

    files_diff = {}
    if UPDATE_ALL:
        files_diff = get_full_tree()
    elif last_version != [0, 0, 0]:
        files_diff = get_diff(encode_version(last_version), LATEST_TAG)

    if len(files_diff):
        versions.append((parse_version(LATEST_TAG), {'version': LATEST_TAG, 'update_files': files_diff}))
        with open(os.path.abspath(os.path.join(myPath.WORK_DIR, 'version.json')), 'w') as file:
            temp = {}
            for (version, version_info) in versions:
                temp[encode_version(version)] = version_info
            file.write(json.dumps(temp, indent=4))

    subprocess.run(f'git checkout {cur_branch}', shell=True, stdout=subprocess.PIPE)


if __name__ == '__main__':
    main()
