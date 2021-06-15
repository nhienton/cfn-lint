import logging

import cfnlint.core
import cfnlint.registry
from test.testlib.testcase import BaseTestCase

from mock import patch

LOGGER = logging.getLogger('cfnlint')


class MyTestAWSCallRegistry(BaseTestCase):
    """Test AWS call registry """

    @patch('subprocess.check_output')
    @patch('cfnlint.registry.Registry.create_schema_file')
    @patch('cfnlint.registry.Registry.create_metadata_file')
    def test_aws_call(self, create_metadata, create_schema, mock_subprocess):
        filename = 'test/fixtures/templates/good/generic.yaml'
        (args, filenames, _) = cfnlint.core.get_args_filenames(['--template', filename])
        (template, rules, _) = cfnlint.core.get_template_rules(filename, args)
        registry = cfnlint.registry.Registry(filename, template, ['us-east-1'])

        mock_subprocess.return_value = '{"NotSchema": "NotSchema", "Schema": "Schema"}'

        metadata, schema = registry.aws_call_registry('us-east-1', 'AWS::ECS::Cluster', 'RESOURCE', 'test-path')
        create_schema.asser_called_once()
        create_metadata.asser_called_once()
        self.assertEqual(metadata, {"NotSchema": "NotSchema"})
        self.assertEqual(schema, {"Schema": "Schema"})
