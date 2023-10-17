import unittest

from smi_python_commons.arguments.config import Config
from smi_python_commons.arguments.constants import SMI_PROFILES_ARGUMENT, SMI_CONFIG_PATHS_ARGUMENT, \
    SMI_OPTIONAL_CONFIG_FILES_ARGUMENT
from smi_python_commons.config.application import Application, find_last_not_none_and_empty
from smi_python_commons.environment.variables import set_environment_variable, delete_environment_variable


class IntegrationTestApplication(unittest.TestCase):

    def setUp(self):
        delete_environment_variable("SMI_PROFILES")
        delete_environment_variable("SMI_CONFIG_PATHS")
        delete_environment_variable("SMI_OPTIONAL_CONFIG_FILES")
        set_environment_variable("SOME_NUMBER_VALUE_A", "123")
        set_environment_variable("SOME_NUMBER_VALUE_B", "123.456")
        set_environment_variable("SOME_BOOLEAN_VALUE_A", "true")
        set_environment_variable("SOME_BOOLEAN_VALUE_B", "false")
        set_environment_variable("SOME_STRING_VALUE_A", "A AA AAA")
        set_environment_variable("SOME_STRING_VALUE_B", "B BB BBB")

    def test_init_default_profiles(self):
        argv = ["example_application_name.py"]
        argv_config = Config(
            'Example parser',
            [
                SMI_PROFILES_ARGUMENT,
                SMI_CONFIG_PATHS_ARGUMENT
            ])
        app = Application(argv, argv_config)
        self.assertEqual(app.profiles_list, [])
        self.assertEqual(app.default_application_files, ['application.json', 'application.yml', 'application.yaml'])
        self.assertEqual(app.application_files, ['application.json', 'application.yml', 'application.yaml'])
        self.assertEqual(app.config_paths, ['./test/resources', './resources'])
        self.assertEqual(
            app.applications_files_paths,
            [['./test/resources/application.yaml',
              {'a': {'b': {'c': 'application.yaml',
                           'd': 123,
                           'e': 123.456,
                           'f': True,
                           'g': False,
                           'h': 'A AA AAA',
                           'i': 'B BB BBB',
                           'j': '${NON_EXISTING_VALUE}'},
                     'd': 123,
                     'e': 123.456,
                     'f': True,
                     'g': False,
                     'h': 'A AA AAA',
                     'i': 'B BB BBB',
                     'j': '${NON_EXISTING_VALUE}'},
               'name': './test/resources/application.yaml'}]
             ]
        )
        self.assertEqual(app.merged_config, {'a': {'b': {'c': 'application.yaml',
                                                         'd': 123,
                                                         'e': 123.456,
                                                         'f': True,
                                                         'g': False,
                                                         'h': 'A AA AAA',
                                                         'i': 'B BB BBB',
                                                         'j': '${NON_EXISTING_VALUE}'},
                                                   'd': 123,
                                                   'e': 123.456,
                                                   'f': True,
                                                   'g': False,
                                                   'h': 'A AA AAA',
                                                   'i': 'B BB BBB',
                                                   'j': '${NON_EXISTING_VALUE}'},
                                             'name': './test/resources/application.yaml'})

    def test_init_cli_profiles(self):
        set_environment_variable("SMI_PROFILES", "profileX,profileY")
        set_environment_variable("SMI_CONFIG_PATHS", "./test/resources/env")
        set_environment_variable("SMI_OPTIONAL_CONFIG_FILES", "./test/resources/env/optional.yaml")
        argv = [
            "example_application_name.py",
            '--smi-profiles', 'profile1,profile2',
            '--smi-config-paths', './test/resources/cli',
            '--smi-optional-config-files', './test/resources/cli/optional.yaml']
        argv_config = Config(
            'Example parser',
            [
                SMI_PROFILES_ARGUMENT,
                SMI_CONFIG_PATHS_ARGUMENT,
                SMI_OPTIONAL_CONFIG_FILES_ARGUMENT
            ])
        app = Application(argv, argv_config)
        self.assertEqual(app.profiles_list, ['profile1', 'profile2'])
        self.assertEqual(app.default_application_files, ['application.json', 'application.yml', 'application.yaml'])
        self.assertEqual(
            app.application_files,
            [
                'application.json',
                'application.yml',
                'application.yaml',
                'application-profile1.json',
                'application-profile1.yml',
                'application-profile1.yaml',
                'application-profile2.json',
                'application-profile2.yml',
                'application-profile2.yaml'
            ]
        )
        self.assertEqual(
            app.config_paths,
            [
                './test/resources',
                './resources',
                './test/resources/env',
                './test/resources/cli'
            ]
        )
        self.assertEqual(
            app.applications_files_paths,
            [['./test/resources/application.yaml',
              {'a': {'b': {'c': 'application.yaml',
                           'd': 123,
                           'e': 123.456,
                           'f': True,
                           'g': False,
                           'h': 'A AA AAA',
                           'i': 'B BB BBB',
                           'j': '${NON_EXISTING_VALUE}'},
                     'd': 123,
                     'e': 123.456,
                     'f': True,
                     'g': False,
                     'h': 'A AA AAA',
                     'i': 'B BB BBB',
                     'j': '${NON_EXISTING_VALUE}'},
               'name': './test/resources/application.yaml'}],
             ['./test/resources/env/application.yaml',
              {'d': {'e': {'f': 'env/application.yaml'}},
               'name': './test/resources/env/application.yaml'}],
             ['./test/resources/cli/application.yaml',
              {'g': {'h': {'i': 'cli/application.yaml'}},
               'name': './test/resources/cli/application.yaml'}],
             ['./test/resources/env/optional.yaml',
              {'a': {'k': {'l': 'Some optional value from environment optional yaml'}}}],
             ['./test/resources/cli/optional.yaml',
              {'a': {'k': {'l': 'Some optional value from CLI optional yaml'}}}]]
        )
        self.assertEqual(app.merged_config,
                         {'a':
                              {'b':
                                   {'c': 'application.yaml',
                                    'd': 123,
                                    'e': 123.456,
                                    'f': True,
                                    'g': False,
                                    'h': 'A AA AAA',
                                    'i': 'B BB BBB',
                                    'j': '${NON_EXISTING_VALUE}'},
                               'd': 123,
                               'e': 123.456,
                               'f': True,
                               'g': False,
                               'h': 'A AA AAA',
                               'i': 'B BB BBB',
                               'j': '${NON_EXISTING_VALUE}',
                               'k': {'l': 'Some optional value from CLI optional yaml'}},
                          'd': {'e': {'f': 'env/application.yaml'}},
                          'g': {'h': {'i': 'cli/application.yaml'}},
                          'name': './test/resources/cli/application.yaml'
                          }
                         )

    def test_init_environment_profiles(self):
        set_environment_variable("SMI_PROFILES", "profileX,profileY")
        set_environment_variable("SMI_CONFIG_PATHS", "./test/resources/env")
        set_environment_variable("SMI_OPTIONAL_CONFIG_FILES", "./test/resources/env/optional.yaml")
        argv = ["example_application_name.py"]
        argv_config = Config(
            'Example parser',
            [
                SMI_PROFILES_ARGUMENT,
                SMI_CONFIG_PATHS_ARGUMENT
            ])
        app = Application(argv, argv_config)
        self.assertEqual(app.profiles_list, ['profileX', 'profileY'])
        self.assertEqual(app.default_application_files, ['application.json', 'application.yml', 'application.yaml'])
        self.assertEqual(
            app.application_files,
            [
                'application.json',
                'application.yml',
                'application.yaml',
                'application-profileX.json',
                'application-profileX.yml',
                'application-profileX.yaml',
                'application-profileY.json',
                'application-profileY.yml',
                'application-profileY.yaml'
            ]
        )
        self.assertEqual(app.config_paths, ['./test/resources', './resources', './test/resources/env'])
        self.assertEqual(
            app.applications_files_paths,
            [['./test/resources/application.yaml',
              {'a': {'b': {'c': 'application.yaml',
                           'd': 123,
                           'e': 123.456,
                           'f': True,
                           'g': False,
                           'h': 'A AA AAA',
                           'i': 'B BB BBB',
                           'j': '${NON_EXISTING_VALUE}'},
                     'd': 123,
                     'e': 123.456,
                     'f': True,
                     'g': False,
                     'h': 'A AA AAA',
                     'i': 'B BB BBB',
                     'j': '${NON_EXISTING_VALUE}'},
               'name': './test/resources/application.yaml'}],
             ['./test/resources/env/application.yaml',
              {'d': {'e': {'f': 'env/application.yaml'}},
               'name': './test/resources/env/application.yaml'}],
             ['./test/resources/env/optional.yaml', {
                 'a': {'k': {'l': 'Some optional value from environment optional yaml'}}}]
             ]
        )
        self.assertEqual(
            app.merged_config,
            {'a':
                 {'b':
                      {'c': 'application.yaml',
                       'd': 123,
                       'e': 123.456,
                       'f': True,
                       'g': False,
                       'h': 'A AA AAA',
                       'i': 'B BB BBB',
                       'j': '${NON_EXISTING_VALUE}'
                       },
                  'd': 123,
                  'e': 123.456,
                  'f': True,
                  'g': False,
                  'h': 'A AA AAA',
                  'i': 'B BB BBB',
                  'j': '${NON_EXISTING_VALUE}',
                  'k': {'l': 'Some optional value from environment optional yaml'},
                  },
             'd':
                 {'e':
                      {'f': 'env/application.yaml'}
                  },
             'name': './test/resources/env/application.yaml'
             }
        )

    def test_find_last_not_none(self):
        result = find_last_not_none_and_empty(None, ["1", "2"], None, ["3", "4"])
        self.assertEqual(result, ['3', '4'])
        result = find_last_not_none_and_empty(None, None, None)
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
