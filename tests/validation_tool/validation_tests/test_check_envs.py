import unittest
from unittest import mock

from amazon_emr_serverless_image_cli.helper import logging
from amazon_emr_serverless_image_cli.validation_tool.validation_models.validation_models import \
    EnvironmentVariable
from amazon_emr_serverless_image_cli.validation_tool.validation_tests.check_envs import \
    CheckEnvs
from tests.lib.utils import INSPECT


class TestEnvs(unittest.TestCase):
    def setUp(self) -> None:
        self.log = logging.Log()
        self.inspect = INSPECT
        self.env_list = ["env1", "env2", "env3"]
        self.envs = [EnvironmentVariable("env1", "env1", "path1"),
            EnvironmentVariable("env2", "env2", "path2"),
            EnvironmentVariable("env3", "env3", None)]

    def test_match(self):
        env_vars = {'env1': 'path1', 'env2': 'path2', 'env3': 'path3'}
        env_path = self.inspect['Config']['Env']
        env_check_instance = CheckEnvs(
            env_path, self.env_list, self.envs, self.log)

        with self.assertLogs(self.log.log) as t:
            result = env_check_instance.match(env_vars)
            self.assertEqual(result, 1)
        expected = 'INFO:logger:env1 is set with value: path1 : PASS'
        self.assertIn(expected, t.output)
        expected = 'INFO:logger:env2 is set with value: path2 : PASS'
        self.assertIn(expected, t.output)
        expected = 'INFO:logger:env3 is set with value: path3 : PASS'
        self.assertIn(expected, t.output)

        env_vars['env2'] = 'path3'
        with self.assertLogs(self.log.log) as t:
            result = env_check_instance.match(env_vars)
            self.assertEqual(result, 0)
        expected = 'INFO:logger:env1 is set with value: path1 : PASS'
        self.assertIn(expected, t.output)
        expected = 'ERROR:logger:env2 MUST set to path2 : FAIL'
        self.assertIn(expected, t.output)
        expected = 'INFO:logger:env3 is set with value: path3 : PASS'
        self.assertIn(expected, t.output)

        del env_vars['env3']
        with self.assertLogs(self.log.log) as t:
            result = env_check_instance.match(env_vars)
            self.assertEqual(result, 0)
        expected = 'INFO:logger:env1 is set with value: path1 : PASS'
        self.assertIn(expected, t.output)
        expected = 'ERROR:logger:env2 MUST set to path2 : FAIL'
        self.assertIn(expected, t.output)
        expected = 'ERROR:logger:env3 MUST be set : FAIL'
        self.assertIn(expected, t.output)

    @mock.patch('amazon_emr_serverless_image_cli.validation_tool.validation_tests.check_envs.CheckEnvs.match')
    def test_check(self, match):
        env_path = self.inspect['Config']['Env']
        env_check_instance = CheckEnvs(
            env_path, self.env_list, self.envs, self.log)

        match.return_value = 1
        actual = env_check_instance.check()
        expected = {'env1': 'path1', 'env2': 'path2'}
        match.assert_called_once_with(expected)
        self.assertEqual(actual, 1)
