import os
import unittest
from unittest import mock

import yaml

from amazon_emr_serverless_image_cli.helper import manifest_reader


class TestManifestReader(unittest.TestCase):
    def test_load_yaml(self):
        yaml.load = mock.MagicMock(
            return_value={"Test": {"ValidationTool": "AWSValidationTool"}})
        with mock.patch("builtins.open", mock.mock_open(read_data="yaml_file")):
            actual = manifest_reader.load_yaml("yaml_file")
            expected = dict()
            expected['Test'] = dict()
            expected['Test']['ValidationTool'] = "AWSValidationTool"
            yaml.load.assert_called_once()
            self.assertEqual(actual, expected)
