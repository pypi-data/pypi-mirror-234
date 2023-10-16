#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime
import os
import pathlib
import platform
import shlex
import shutil
import subprocess
import sys

from distutils.version import LooseVersion


def get_rc(path):
    return """
# @Neulabs (configured in %s)
source %s/.env
# config end
""" % (datetime.datetime.now(), path)


def argsinstance():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--sync',
        action='store_true',
        default=False,
        help='Sync bin folder',
    )
    return parser


def getenv():
    check_python_version()

    env = {key: pathlib.Path(value) for key, value in os.environ.items() if key.startswith('NEULABS_')}

    if not env:
        raise Exception('NEULABS_ env variables not found')

    if os.getenv('NEULABS_DEBUG') == 'true':
        basepath = str(pathlib.Path(os.getenv('NEULABS_PATH'), '.debug', '.neulabs-cli'))
        for key, value in env.items():
            env[key] = pathlib.Path(str(value).replace(os.getenv('NEULABS_PATH'), basepath))

    return env


def configurations(env: dict):
    if os.path.isdir(env['NEULABS_PATH']):
        print(f'Neulabs already installed in {env["NEULABS_PATH"]}')
        response = input('Press Enter to continue...')
        if response != '':
            exit(0)

    os.makedirs(f"{env['NEULABS_PATH']}", exist_ok=True)
    os.makedirs(f"{env['NEULABS_MODULES_PATH']}", exist_ok=True)

    if os.path.isfile(env['NEULABS_ENV_PATH']) is True:
        os.rename(env['NEULABS_ENV_PATH'], str(
            env['NEULABS_ENV_PATH']) + '.old')

    with open(env['NEULABS_ENV_PATH'], 'w') as f:
        for key, value in env.items():
            f.write(f'export {key}={value}\n')

    print('Check in .bashrc or/and .zshrc file: \n' + get_rc(env['NEULABS_PATH']) + '\n')

    bashrc_path = os.path.join(os.path.expanduser('~'), '.bashrc')
    if os.path.isfile(bashrc_path):
        with open(bashrc_path, 'r') as f:
            if '@Neulabs' not in f.read():
                with open(bashrc_path, 'a') as f:
                    f.write(get_rc(env['NEULABS_PATH']))

    zshrc_path = os.path.join(os.path.expanduser('~'), '.zshrc')
    if os.path.isfile(zshrc_path):
        with open(zshrc_path, 'r') as f:
            if '@Neulabs' not in f.read():
                with open(zshrc_path, 'a') as f:
                    f.write(get_rc(env['NEULABS_PATH']))


def rsync_files(dirpath):
    print('Sync folder')
    for file_name in os.listdir(dirpath):
        path = pathlib.Path(dirpath, file_name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        if os.path.isfile(path):
            os.remove(path)
        print(f'Remove {path}')


def copy_files(source_dirpath, dest_dirpath):
    for file_name in os.listdir(source_dirpath):
        source = pathlib.Path(source_dirpath, file_name)
        destination = pathlib.Path(dest_dirpath, file_name)
        if os.path.isfile(source):
            shutil.copy(source, destination)
            print(f'Copied {file_name} in {destination}')


def copy(dest_dirpath, source_dirpath, sync=False):
    if not os.path.isdir(dest_dirpath):
        os.makedirs(dest_dirpath, exist_ok=True)

    if os.path.isfile(source_dirpath):
        shutil.copy(source_dirpath, dest_dirpath)
        print(f'Copied {os.path.basename(source_dirpath)} in {dest_dirpath}')
        return

    if sync:
        rsync_files(dest_dirpath)
    copy_files(source_dirpath=source_dirpath, dest_dirpath=dest_dirpath)


def check_python_version():
    if LooseVersion(platform.python_version()) < '3.8':
        raise RuntimeError('PY Version required >= 3.8')


def main():
    try:
        args = argsinstance().parse_args()
        source_path = os.path.dirname(pathlib.Path(__file__).parent.resolve())

        env = getenv()

        configurations(env)

        copy(
            dest_dirpath=env['NEULABS_PATH'],
            source_dirpath=pathlib.Path(source_path, 'Taskfile.yml'),
        )

        if os.path.isfile(env['NEULABS_TASKFILE_LOCAL_CLI_PATH']) is False:
            copy(
                dest_dirpath=env['NEULABS_PATH'],
                source_dirpath=pathlib.Path(source_path, 'Taskfile.local.yml'),
            )

        copy(
            dest_dirpath=env['NEULABS_MODULES_PATH'],
            source_dirpath=pathlib.Path(source_path, 'neucli'),
            sync=args.sync
        )

        copy(
            dest_dirpath=env['NEULABS_TASKFILES_PATH'],
            source_dirpath=pathlib.Path(source_path, 'taskfiles/cli'),
            sync=args.sync
        )

        if not os.path.isdir(env['NEULABS_LIB_PATH']):
            try:
                cmd = f'git clone git@github.com:neulabscom/neulabs-cli-modules.git {env["NEULABS_PATH"]}/lib'
                subprocess.check_call(shlex.split(cmd))
            except Exception:
                cmd = f'git clone https://github.com/neulabscom/neulabs-cli-modules.git {env["NEULABS_PATH"]}/lib'
                subprocess.check_call(shlex.split(cmd))
        else:
            pwd = os.getcwd()
            os.chdir(env['NEULABS_LIB_PATH'])
            subprocess.check_call(shlex.split('git checkout main'))
            subprocess.check_call(shlex.split('git pull'))
            os.chdir(pwd)
    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    sys.exit(main())
