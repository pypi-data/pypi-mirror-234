#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import pathlib
import shlex
import shutil
import subprocess
import sys

DOCS_PATH = os.path.join(os.environ['NEULABS_LIB_PATH'], 'modules', 'docs')
RUNNERS_PATH = os.path.join(
    os.environ['NEULABS_LIB_PATH'], 'modules', 'runners')
ACTIONS_PATH = os.path.join(
    os.environ['NEULABS_LIB_PATH'], 'modules', 'actions')


def argsinstance():
    def _cmd_docs(parser):
        subparsers = parser.add_parser(
            'docs', help='Create docs template')

        subparsers.add_argument('-n', '--repository-name',
                                required=True, help='Name of the repository')

    def _cmd_runners(parser):
        parser.add_parser(
            'runners', help='Create runners template')

    def _cmd_actions(parser):
        subparsers = parser.add_parser(
            'actions', help='Create runners template')

        choices_type = ['terraform-module'
                        'dart',
                        'elixir',
                        'go',
                        'helm',
                        'java',
                        'krm',
                        'maven',
                        'node',
                        'expo',
                        'ocaml',
                        'php',
                        'python',
                        'ruby',
                        'rust',
                        'sfdx',
                        'simple',
                        ]
        subparsers.add_argument('--repository-type', type=str, choices=choices_type, required=True, help='Repository type')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Help for command', dest='command')

    parser.add_argument('--branch', default='main', help='Branch name')
    parser.add_argument('-d', '--dest-path', default='',
                        help='Destination path')

    _cmd_docs(subparsers)
    _cmd_runners(subparsers)
    _cmd_actions(subparsers)

    return parser


def pull_lib(branch_name: str):
    pwd = os.getcwd()
    os.chdir(os.environ['NEULABS_LIB_PATH'])
    subprocess.call(shlex.split(f'git checkout {branch_name}'))
    subprocess.call(shlex.split(f'git pull'))
    os.chdir(pwd)


def copy_files(source_dirpath, dest_dirpath):
    if not os.path.isdir(dest_dirpath):
        os.makedirs(dest_dirpath)

    for file_name in os.listdir(source_dirpath):
        source = pathlib.Path(source_dirpath, file_name)
        destination = pathlib.Path(dest_dirpath, file_name)
        shutil.copy(source, destination)
        print(f'Copied {file_name} in {destination}')


def subsitute_in_file(file_path, old_string, new_string):
    with open(file_path, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace(old_string, new_string)

    with open(file_path, 'w') as file:
        file.write(filedata)


def lib_docs(base_dest_path: str, repository_name: str):
    docs_source_path = os.path.join(DOCS_PATH, 'files')
    docs_dest_path = os.path.join(base_dest_path, 'docs')
    print(
        f'Copying docs files from {docs_source_path} to {docs_dest_path}')
    shutil.copytree(docs_source_path, docs_dest_path, dirs_exist_ok=True)

    scripts_source_path = os.path.join(DOCS_PATH, 'scripts')
    scripts_dest_path = os.path.join(base_dest_path, '.github', 'scripts')
    print(
        f'Copying scripts files from {scripts_source_path} to {scripts_dest_path}')
    copy_files(scripts_source_path, scripts_dest_path)

    workflows_source_path = os.path.join(DOCS_PATH, 'workflows')
    workflows_dest_path = os.path.join(
        base_dest_path, '.github', 'workflows')
    print(
        f'Copying workflows files from {workflows_source_path} to {workflows_dest_path}')
    copy_files(workflows_source_path, workflows_dest_path)

    files = ['docs/docusaurus.config.js',
             '.github/workflows/deploy-docs.yml']
    for file in files:
        subsitute_in_file(os.path.join(base_dest_path, file),
                          '%NAME%', repository_name)


def lib_runners(base_dest_path: str):
    scripts_source_path = os.path.join(RUNNERS_PATH, 'scripts')
    scripts_dest_path = os.path.join(base_dest_path, '.github', 'scripts')
    print(
        f'Copying scripts files from {scripts_source_path} to {scripts_dest_path}')
    copy_files(scripts_source_path, scripts_dest_path)


def lib_actions(base_dest_path: str, repository_type: str):
    files_source_path = os.path.join(ACTIONS_PATH, 'files')
    files_dest_path = os.path.join(base_dest_path)
    print(
        f'Copying files from {files_source_path} to {files_dest_path}')
    shutil.copytree(files_source_path, files_dest_path, dirs_exist_ok=True)

    workflows_source_path = os.path.join(ACTIONS_PATH, 'workflows')
    workflows_dest_path = os.path.join(base_dest_path, '.github')
    print(
        f'Copying workflows files from {workflows_source_path} to {workflows_dest_path}')
    shutil.copytree(workflows_source_path,
                    workflows_dest_path, dirs_exist_ok=True)

    files = ['release-please-cofig.json']
    for file in files:
        subsitute_in_file(os.path.join(base_dest_path, file),
                          '%RELEASE_TYPE%', repository_type)


def main():
    try:
        args = argsinstance().parse_args()
        pull_lib(args.branch)

        base_dest_path = os.path.join(
            os.environ['NEULABS_EXECUTION_CLI_PATH'], args.dest_path)

        if args.command == 'docs':
            return lib_docs(base_dest_path, args.repository_name)

        if args.command == 'runners':
            return lib_runners(base_dest_path)

        if args.command == 'actions':
            return lib_actions(base_dest_path, args.repository_type)

    except KeyboardInterrupt:
        return 0


if __name__ == '__main__':
    sys.exit(main())
