import unittest

from smi_python_commons.arguments.argument import Argument
from smi_python_commons.arguments.config import Config
from smi_python_commons.arguments.constants import SMI_PROFILES_ARGUMENT
from smi_python_commons.arguments.parser import parse_arguments


class TestParser(unittest.TestCase):

    def test_parse_arguments(self):
        argv = ["example_application_name.py", '-i', 'input.txt', '-o', 'output.txt', '--smi-profiles',
                'profile1,profile2']
        argv_config = Config(
            'Example parser',
            [
                Argument('input', 'i', str, 'Input file', True),
                Argument('output', 'o', str, 'Output file', True),
                SMI_PROFILES_ARGUMENT
            ])

        parsed = parse_arguments(argv, argv_config)

        self.assertEqual(parsed.input, 'input.txt')
        self.assertEqual(parsed.output, 'output.txt')
        self.assertEqual(parsed.smi_profiles, ['profile1', 'profile2'])


if __name__ == '__main__':
    unittest.main()
