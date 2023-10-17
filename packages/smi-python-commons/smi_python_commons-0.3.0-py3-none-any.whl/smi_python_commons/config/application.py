import os
import re
from functools import reduce

from smi_python_commons.arguments.config import Config
from smi_python_commons.arguments.parser import parse_arguments
from smi_python_commons.config.constants import SMI_CONFIG_PATHS, SMI_PROFILES, APPLICATION_FILE_SUFFIXES, \
    SMI_OPTIONAL_CONFIG_FILES, \
    APPLICATION_FILE_PREFIXES, SMI_NAME
from smi_python_commons.environment.variables import get_environment_variables_list, get_environment_variable
from smi_python_commons.json.parser import parse_json_file
from smi_python_commons.string.operations import combined_list, combined_by_function_list, find_named_placeholders, \
    replace_named_placeholder
from smi_python_commons.yaml.parser import parse_yaml_file


class Application:

    def __init__(self, argv: [str], argv_config: Config):
        self.argv = argv
        self.argv_config = argv_config
        self.arguments = parse_arguments(self.argv, self.argv_config)
        # get resource/config folders in order and loading (overload in case of existing file) by that
        # order: code, env, cli
        # Lists orders represent overload order
        self.config_paths = list(
            ["./test/resources", "./resources"] +
            get_environment_variables_list(SMI_CONFIG_PATHS) +
            self.get_cli_config_paths()
        )
        # get profiles in order and overload by that order: (code, ) env, cli
        self.profiles_list = find_last_not_none_and_empty(
            get_environment_variables_list(SMI_PROFILES),
            self.arguments.smi_profiles
        )
        self.default_application_files = combined_list(
            APPLICATION_FILE_PREFIXES,
            APPLICATION_FILE_SUFFIXES,
            "."
        )
        application_profiles_file_prefixes = combined_list(
            APPLICATION_FILE_PREFIXES,
            self.profiles_list,
            "-"
        )
        application_profiles_files = combined_list(
            application_profiles_file_prefixes,
            APPLICATION_FILE_SUFFIXES,
            "."
        )
        self.application_files = self.default_application_files + application_profiles_files
        optional_env_application_files = get_environment_variables_list(SMI_OPTIONAL_CONFIG_FILES)
        optional_cli_application_files = self.get_cli_optional_config_files()
        self.applications_files_paths = list(
            map(
                lambda item: [item, self.parse_file_by_type(item)],
                combined_by_function_list(
                    self.config_paths,
                    self.application_files,
                    "/",
                    lambda file_path: os.path.isfile(file_path)
                ) +
                optional_env_application_files +
                optional_cli_application_files
            )
        )
        self.merged_config = reduce(
            lambda x, y: merge_dicts(x, y),
            list(
                map(
                    lambda sub_list: sub_list[1],
                    self.applications_files_paths
                )
            ),
            {}  # initial value
        )
        self.name = "default" or get_environment_variable(SMI_NAME) or self.merged_config["name"] or self.get_cli_name()

    def get_cli_name(self):
        if hasattr(self.arguments, "smi_name") and self.arguments.smi_name is not None:
            return self.arguments.smi_name
        return []

    def get_cli_config_paths(self):
        if hasattr(self.arguments, "smi_config_paths") and self.arguments.smi_config_paths is not None:
            return self.arguments.smi_config_paths
        return []

    def get_cli_optional_config_files(self):
        if hasattr(self.arguments,
                   "smi_optional_config_files") and self.arguments.smi_optional_config_files is not None:
            return self.arguments.smi_optional_config_files
        return []

    @staticmethod
    def parse_file_by_type(file_name: str):
        new_file_name = file_name.lower()
        if re.search(r'\.(yaml|yml)$', new_file_name):
            return parse_yaml_file(file_name, {'post_read_function': post_read_function})
        elif re.search(r'\.json$', new_file_name):
            return parse_json_file(file_name, {'post_read_function': post_read_function})
        else:
            return None


def post_read_function(text: str):
    placeholders = find_named_placeholders(text)
    placeholder_value_pairs = list(
        map(
            lambda place_holder: [place_holder, get_environment_variable(place_holder)],
            placeholders
        )
    )
    for placeholder_value_pair in placeholder_value_pairs:
        placeholder = placeholder_value_pair[0]
        value = placeholder_value_pair[1]
        if value is not None:
            text = replace_named_placeholder(text, placeholder, value)
    return text


def find_last_not_none_and_empty(*args):
    last_not_none = []
    for arg in args:
        if arg is not None and isinstance(arg, list) and arg:
            last_not_none = arg
    return last_not_none


def merge_dicts(dict1, dict2):
    """
    Merge two dictionaries hierarchically.

    Args:
        dict1 (dict): First dictionary.
        dict2 (dict): Second dictionary.

    Returns:
        dict: Merged dictionary.
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result
