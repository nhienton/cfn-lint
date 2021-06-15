import logging

import cfnlint.core
import cfnlint.registry
from test.testlib.testcase import BaseTestCase

from mock import patch

LOGGER = logging.getLogger('cfnlint')


class MyTestCreateFolder(BaseTestCase):
    """Test Create Folder """

    @patch('os.makedirs')
    @patch('cfnlint.registry.Registry.aws_call_registry')
    def test_create_folder(self, aws_call, makedirs):

        filename = 'test/fixtures/templates/good/generic.yaml'
        (args, filenames, _) = cfnlint.core.get_args_filenames(['--template', filename])
        (template, rules, _) = cfnlint.core.get_template_rules(filename, args)
        registry = cfnlint.registry.Registry(filename, template, ['us-east-1'])

        registry.create_folder('/test-path', 'us-east-1', 'TEST', 'MODULE')
        aws_call.asser_called_once()

    @patch('cfnlint.registry.Registry.aws_call_registry')
    def test_create_folder_already_existing(self, aws_call):

        filename = 'test/fixtures/templates/good/generic.yaml'
        (args, filenames, _) = cfnlint.core.get_args_filenames(['--template', filename])
        (template, rules, _) = cfnlint.core.get_template_rules(filename, args)
        registry = cfnlint.registry.Registry(filename, template, ['us-east-1'])
        err = None
        try:
            registry.create_folder('/', 'us-east-1', 'TEST', 'MODULE')
        except OSError as e:
            err = e
        assert(type(err) == OSError)

