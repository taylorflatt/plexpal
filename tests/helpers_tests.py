#!/usr/bin/env python3
# unit test dependencies
import os, sys
import unittest
import json
from unittest import TestCase, mock, main as run_suite
from unittest.mock import patch, Mock, MagicMock
from src.helpers.errors import get_exception
from tests.helpers.context import test_context, class_context
from tests.helpers.asserts import assert_all
import tests.helpers.runner as runner
# suite dependencies
import src, uuid
import traceback
from src.helpers.config import Config
from src.helpers.apireference import API
from src.helpers.config import Config
from src.helpers.enum import _BUILDENUM, ENUM
from src.helpers.errors import Missing_Config, Unhandled, Uncaught


class APIReferenceTests(TestCase):

    mock_config = dict()

    @classmethod
    def setUpClass(cls):
        print("\n", cls.__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.mock_config = {
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

    def tearDown(self):
        self.mock_config = dict()

    @patch.object(uuid, "uuid4", return_value=Mock(), side_effect=Exception())
    def test_instantiation_raises_unhandled_exception_if_not_attribute_error(self, mock_dict):
        return assert_all([(self.assertRaises, Unhandled, API, "plex")], test_context())

    @patch.object(src.helpers.config.Config, "get_dict", return_value=dict())
    def test_instantiation_raises_when_bad_config(self, mock_config_object):
        return assert_all([(self.assertRaises, AttributeError, API, "plex")], test_context())

    @patch.object(src.helpers.config.Config, "get_dict", return_value=Config.BAD_PATH)
    def test_instantiation_raises_when_bad_config_path(self, mock_config_object):
        return assert_all([(self.assertRaises, Missing_Config, API, "plex")], test_context())

    @patch.object(src.helpers.config.Config, "get_dict")
    def test_instantiation_succeeds(self, mock_config_object):
        mock_config_object.return_value = self.mock_config
        sut = API("plex")

        self.assertIsNotNone(sut.headers)  # pylint:disable=no-member
        plex_client_identifier = sut.headers.get("X-Plex-Client-Identifier")  # pylint:disable=no-member
        return assert_all(
            (
                (self.assertEqual, "mockProduct", sut.headers.get("X-Plex-Product")), # pylint:disable=no-member
                (self.assertEqual, "https://fake.authurl.tv", sut.authentication_url), # pylint:disable=no-member
                (self.assertNotEqual, "<UUID>", plex_client_identifier),
                (self.assertIsInstance, plex_client_identifier, uuid.UUID),
                (mock_config_object.assert_called_once,)
            ),
            test_context()
        )


class ConfigTests(TestCase):

    real_config = dict()
    good_config_path = str()
    bad_config_path = str()

    @classmethod
    def setUpClass(cls):
        print("\n", cls.__name__)
        abs_dir_path = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]
        cls.good_config_path = os.path.join(abs_dir_path, os.path.relpath("src/helpers/config/api.conf"))
        cls.bad_config_path = "fake_path"
        with open(cls.good_config_path, "r") as cfg:
            cls.real_config = json.loads(cfg.read())

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.sut = Config(self.good_config_path)

    def test_instantiation_succeeds(self):
        return assert_all(
            (
                (self.assertNotEqual,
                 self.sut.path,
                 Config.BAD_PATH),
                (self.assertGreater,
                 len(self.sut.config.items()),
                 1),
                (self.assertDictEqual,
                 self.sut.config,
                 self.real_config)
            ),
            test_context()
        )

    def test_get_key_succeeds_with_successful_instantiation(self):
        return assert_all(
            (
                (self.assertNotEqual,
                 Config.NO_SUCH_KEY,
                 self.sut.get("sonarr")),
                (self.assertDictEqual,
                 {
                     "headers": {}
                 },
                 self.sut.get("sonarr"))
            ),
            test_context()
        )

    def test_get_dict_succeeds_with_successful_instantiation(self):
        return assert_all(
            (
                (self.assertNotEqual,
                 Config.BAD_PATH,
                 self.sut.get_dict()),
                (self.assertDictEqual,
                 self.real_config,
                 self.sut.get_dict())
            ),
            test_context()
        )

    def test_instantiation_succeeds_with_bad_path(self):
        self.sut = Config(self.bad_config_path)
        return assert_all(
            ((self.assertEqual,
              self.sut.path,
              Config.BAD_PATH),
             (self.assertDictEqual,
              self.sut.config,
              dict())),
            test_context()
        )

    def test_get_with_bad_key_returns_no_such_key(self):
        return assert_all([(self.assertEqual, self.sut.get(123), Config.NO_SUCH_KEY)], test_context())

    def test_get_with_bad_config_throws_unhandled_exception(self):
        self.sut.config = ""
        return assert_all([(self.assertRaises, Unhandled, self.sut.get, "plex")], test_context())

    def test_get_dict_with_bad_path_returns_bad_path(self):
        self.sut = Config(self.bad_config_path)
        return assert_all([(self.assertEqual, self.sut.get_dict(), Config.BAD_PATH)], test_context())


class EnumTests(TestCase):

    @classmethod
    def setUpClass(cls):
        print(cls.__name__)
        cls.sut = _BUILDENUM
        cls.test_dict = {"key1": "value1", "key2": "value2"}

    def setUp(self):
        pass

    def tearDown(self):
        self.sut = _BUILDENUM()

    def test_buildenum_assigns_attributes_successfully(self):
        self.sut.__init__(self.sut, **self.test_dict)
        assert_all(
            (
                (self.assertEqual,
                 self.sut.key1,
                 self.test_dict["key1"]),
                (self.assertEqual,
                 self.sut.key2,
                 self.test_dict["key2"])
            ),
            test_context()
        )

    def test_enum_assigns_attributes_successfully(self):
        sut = ENUM(self.test_dict)
        assert_all(
            (
                (self.assertEqual, sut.key1, self.test_dict["key1"]), # pylint:disable=no-member
                (self.assertEqual, sut.key2, self.test_dict["key2"]) # pylint:disable=no-member
            ),
            test_context()
        )

    def test_buildenum_adds_attributes_successfully(self):
        self.sut.addattr(self.sut, "new", "value")
        self.sut.addattr(self.sut, "another", "one")
        assert_all(
            (
                (self.assertEqual, self.sut.new, "value"), # pylint:disable=no-member
                (self.assertEqual, self.sut.another, "one") # pylint:disable=no-member
            ),
            test_context()
        )

    def test_enum_inherits_from_buildenum(self):
        sut = ENUM(dict())
        assert_all([(self.assertIsInstance, sut, _BUILDENUM)], test_context())

    def test_enum_adds_attributes_successfully(self):
        sut = ENUM(dict())
        sut.addattr("added", "value")
        sut.addattr("boo", "ahh!")
        assert_all(
            (
                (self.assertEqual, sut.added, "value"), # pylint:disable=no-member
                (self.assertEqual, sut.boo, "ahh!") # pylint:disable=no-member
            ),
            test_context()
        )


class ErrorsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        print(cls.__name__)

    def test_exceptions_can_be_raised_properly(self):

        def exc_raiser(exception):
            raise exception

        assert_all(
            (
                (self.assertRaises,
                 Missing_Config,
                 exc_raiser,
                 Missing_Config()),
                (self.assertRaises,
                 Unhandled,
                 exc_raiser,
                 Unhandled()),
                (self.assertRaises,
                 Uncaught,
                 exc_raiser,
                 Uncaught())
            ),
            test_context()
        )

    @patch.object(sys, "exc_info", return_value=("fake_exception", "no_really_its_fake", "this_traces_back_here"))
    def test_get_exception_returns_a_dictionary(self, mock_exception_info):
        exception = get_exception()
        assert_all(
            (
                (self.assertIsInstance,
                 exception,
                 dict),
                (
                    self.assertDictEqual,
                    {
                        "exception": {
                            "type": "fake_exception",
                            "value": "no_really_its_fake"
                        }
                    },
                    exception
                )
            ),
            test_context()
        )

    @patch.object(sys, "exc_info", return_value=("fake_exception", "no_really_its_fake", "this_traces_back_here"))
    def test_get_exception_returns_a_string_when_text_flag_is_enabled(self, mock_exception_info):
        exception_text = get_exception(text=True)
        assert_all(
            (
                (self.assertNotIsInstance,
                 exception_text,
                 dict),
                (self.assertIn,
                 "type: fake_exception",
                 exception_text),
                (self.assertIn,
                 "value: no_really_its_fake",
                 exception_text)
            ),
            test_context()
        )

    @patch.object(sys, "exc_info", return_value=("fake_exception", "no_really_its_fake", "this_traces_back_here"))
    def test_get_exception_adds_description_when_msg_field_is_populated(self, mock_exception_info):
        exception = get_exception("exception_description")
        assert_all([(self.assertEqual, "exception_description", exception.get("description"))], test_context())

    @patch.object(sys, "exc_info", return_value=("fake_exception", "no_really_its_fake", "this_traces_back_here"))
    @patch.object(traceback, "format_tb", return_value="this_traceback\nis_formatted")
    def test_get_exception_adds_traceback_when_trace_flag_is_enabled(self, mock_exception_info, mock_traceback):
        exception_dict = get_exception(trace=True)
        assert_all(
            [(self.assertEqual,
              "this_traceback\nis_formatted",
              exception_dict.get("traceback"))],
            test_context()
        )


if __name__ == "__main__":
    tests = [APIReferenceTests, ConfigTests, EnumTests, ErrorsTests]
    runner.run_tests(tests)
