# -*- coding: utf-8; -*-

import os
from unittest import TestCase

from sqlalchemy import create_engine

from rattail.config import RattailConfig
from rattail.exceptions import ConfigurationError
from rattail.db import Session as RattailSession

from tailbone import app
from tailbone.db import Session as TailboneSession


class TestRattailConfig(TestCase):

    config_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'data', 'tailbone.conf'))

    def tearDown(self):
        # may or may not be necessary depending on test
        TailboneSession.remove()

    def test_settings_arg_must_include_config_path_by_default(self):
        # error raised if path not provided
        self.assertRaises(ConfigurationError, app.make_rattail_config, {})
        # get a config object if path provided
        result = app.make_rattail_config({'rattail.config': self.config_path})
        # nb. cannot test isinstance(RattailConfig) b/c now uses wrapper!
        self.assertIsNotNone(result)
        self.assertTrue(hasattr(result, 'get'))
