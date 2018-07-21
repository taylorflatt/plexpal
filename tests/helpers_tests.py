#!/usr/bin/env python3
# unit test dependencies
import sys, inspect
from unittest import TestCase, mock, main as run_suite
from unittest.mock import patch, Mock, MagicMock
from src.helpers.errors import get_exception
# suite dependencies
import src, uuid
from src.helpers.config import Config
from src.helpers.apireference import API
from src.helpers.errors import Missing_Config, Unhandled
from src.helpers.test_helpers import assert_all

test_context = sys._getframe


def class_context(obj):
    return type(obj).__name__


class APIReferenceTests(TestCase):

    default_api_config = {
        "plex":
            {
                "headers":
                    {
                        "content-type": "application/json",
                        "X-Plex-Client-Identifier": "<UUID>",
                        "X-Plex-Product": "mockProduct",
                        "X-Plex-Version": "v1.23.456.78"
                    },
                "authentication_url": "https://fake.authurl.tv"
            }
    }

    def setUp(self):
        self.mock_config = self.default_api_config

    def tearDown(self):
        self.mock_config = self.default_api_config

    @patch.object(uuid, "uuid4", return_value=Mock(), side_effect=Exception())
    def test_unhandled_exception(self, mock_dict):
        test_name = test_context().f_code.co_name
        print(test_name)
        success = assert_all([(self.assertRaises, Unhandled, API, "plex")], class_context(self))
        print(test_name, success)

    @patch.object(src.helpers.config.Config, "get_dict", return_value=dict())
    def test_raises_when_bad_config(self, mock_config_object):
        test_name = test_context().f_code.co_name
        print(test_name)
        success = assert_all([(self.assertRaises, AttributeError, API, "plex")], class_context(self))
        print(test_name, success)

    @patch.object(src.helpers.config.Config, "get_dict", return_value=Config.BAD_PATH)
    def test_raises_when_bad_config_path(self, mock_config_object):
        test_name = test_context().f_code.co_name
        print(test_name)
        success = assert_all([(self.assertRaises, Missing_Config, API, "plex")], class_context(self))
        print(test_name, success)

    @patch.object(src.helpers.config.Config, "get_dict", return_value=default_api_config)
    def test_instantiation_succeeds(self, mock_config_object):
        test_name = test_context().f_code.co_name
        sut = API("plex")

        print(test_name)
        self.assertIsNotNone(sut.headers)  # pylint:disable=no-member
        plex_client_identifier = sut.headers.get("X-Plex-Client-Identifier")  # pylint:disable=no-member
        success = assert_all(
            (
                (self.assertEqual, "mockProduct", sut.headers.get("X-Plex-Product")), # pylint:disable=no-member
                (self.assertEqual, "https://fake.authurl.tv", sut.authentication_url), # pylint:disable=no-member
                (self.assertNotEqual, "<UUID>", plex_client_identifier),
                (self.assertIsInstance, plex_client_identifier, uuid.UUID)
            ),
            class_context(self)
        )
        print(test_name, success)


class ConfigTests(TestCase):
    pass


class EnumTests(TestCase):
    pass


class ErrorsTests(TestCase):
    pass


if __name__ == "__main__":
    run_suite()
