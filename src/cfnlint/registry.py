"""
Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""

import logging
from cfnlint.template import Template
import boto3
import os
import platform

LOGGER = logging.getLogger(__name__)


class Registry(object):
    """Download schemas if necessary and validate modules"""

    def __init__(
            self, filename, template, regions):
        self.filename = filename
        self.regions = regions
        self.cfn = Template(filename, template, regions)

    # Check if the appropriate folder already exists
    def check_folders(self, module, registry_type):
        account_id = boto3.client('sts').get_caller_identity().get('Account')
        username = None
        path_split = os.getcwd().split('/')
        try:
            index = path_split.index('Users')
            username = path_split[index + 1]
        except IndexError as error:
            print(error)

        is_windows = True if platform.system() == 'win32' else False

        for region in self.regions:
            if is_windows:
                path = "C:/Users/%s/AppData/cloudformation/%s/%s/%s" % (username, account_id, region, module)
            else:
                path = "/Users/%s/.cloudformation/%s/%s/%s" % (username, account_id, region, module)

            if not os.path.isdir(path):
                self.create_folder(path)

    def create_folder(self, path):
        try:
            print(path)
            os.makedirs(path)
        except OSError as error:
            print(error)



