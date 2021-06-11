"""
Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""


import json
import logging
import os
import platform
import subprocess
import boto3
from cfnlint.template import Template


LOGGER = logging.getLogger(__name__)


class Registry(object):
    """Download schemas if necessary and validate modules"""

    def __init__(
            self, filename, template, regions):
        self.filename = filename
        self.regions = regions
        self.cfn = Template(filename, template, regions)

    # Check if the appropriate folder already exists
    def check_folders(self, name, registry_type):
        account_id = boto3.client('sts').get_caller_identity().get('Account')
        username = None
        path_split = os.getcwd().split('/')
        try:
            index = path_split.index('Users')
            username = path_split[index + 1]
        except IndexError as error:
            print(error)

        is_windows = platform.system() == 'win32'

        for region in self.regions:
            if is_windows:
                path = 'C:/Users/%s/AppData/cloudformation/%s/%s/%s' % (username, account_id, region, name)
            else:
                path = '/Users/%s/.cloudformation/%s/%s/%s' % (username, account_id, region, name)

            if not os.path.isdir(path):
                self.create_folder(path, region, name, registry_type)

    def create_folder(self, path, region, name, registry_type):
        try:
            os.makedirs(path)
            self.aws_call_registry(region, name, registry_type, path)
        except OSError as error:
            print(error)

    def aws_call_registry(self, region, name, registry_type, path):
        cmd = ['aws', '--region', region, 'cloudformation', 'describe-type', '--type', registry_type, '--type-name',
               name]

        metadata = {}
        schema = {}

        # Recuperate detailed information about a registered extension
        extension = json.loads(subprocess.check_output(cmd))

        for field in extension:
            if field != 'Schema':
                metadata[field] = extension[field]
            else:
                schema[field] = extension[field]

        self.create_schema_file(schema, path)
        self.create_metadata_file(metadata, path)

    def create_schema_file(self, data, path):
        try:
            with open(path + '/schema.json', 'x') as f:
                json.dump(data, f)
        except OSError as error:
            print(error)

    def create_metadata_file(self, data, path):
        try:
            with open(path + '/metadata.json', 'x') as f:
                json.dump(data, f)
        except OSError as error:
            print(error)
