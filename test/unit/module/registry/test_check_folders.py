import logging

import cfnlint.core
import cfnlint.registry
from test.testlib.testcase import BaseTestCase

from botocore.stub import Stubber
import boto3
from mock import patch

LOGGER = logging.getLogger('cfnlint')


class TestCheckFolders(BaseTestCase):
    """Test Check Folders """

    @patch('cfnlint.registry.Registry.create_folder')
    @patch('os.getcwd')
    # mock the call against cloudformation registry
    def test_check_folder_existing(self, getcwd, create_folder):
        """Test folder doesn't exist (mac/linux)"""
        getcwd.return_value = 'Users/test_user'
        filename = 'test/fixtures/templates/good/generic.yaml'
        (args, filenames, _) = cfnlint.core.get_args_filenames(['--template', filename])
        (template, rules, _) = cfnlint.core.get_template_rules(filename, args)
        registry = cfnlint.registry.Registry(filename, template, ['us-east-1'])

        stubbed_client = boto3.client('sts')
        stubber = Stubber(stubbed_client)
        stubber.add_response("get_caller_identity", {"Account": "000000000000"})
        stubber.activate()
        self.assertEqual(registry.check_folders(stubbed_client, 'TEST', 'MODULE'), '/Users/test_user/.cloudformation/000000000000/us-east-1/TEST')

    @patch('cfnlint.registry.Registry.create_folder')
    @patch('os.getcwd')
    @patch('platform.system')
    def test_check_folder_existing_windows(self, system, getcwd, create_folder):
        """Test folder doesnt' exist (windows)"""
        getcwd.return_value = 'Users/test_user'
        filename = 'test/fixtures/templates/good/generic.yaml'
        (args, filenames, _) = cfnlint.core.get_args_filenames(['--template', filename])
        (template, rules, _) = cfnlint.core.get_template_rules(filename, args)
        registry = cfnlint.registry.Registry(filename, template, ['us-east-1'])

        stubbed_client = boto3.client('sts')
        stubber = Stubber(stubbed_client)
        stubber.add_response("get_caller_identity", {"Account": "000000000000"})
        stubber.activate()
        system.return_value = 'win32'
        self.assertEqual(registry.check_folders(stubbed_client, 'TEST', 'MODULE'), 'C:/Users/test_user/AppData/cloudformation/000000000000/us-east-1/TEST')


