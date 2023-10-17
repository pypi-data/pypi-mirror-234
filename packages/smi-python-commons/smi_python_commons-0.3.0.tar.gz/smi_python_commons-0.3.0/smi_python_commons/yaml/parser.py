import yaml

from smi_python_commons.file.operations import read_file


def parse_yaml_file(file_name: str, post_actions={}):
    """
    Parse YAML data from a file with optional post-processing actions.

    Args:
        file_name (str): The path to the YAML file to parse.
        post_actions (dict, optional): A dictionary containing post-processing functions for
            'post_read_function' and 'post_parse_function'. Defaults to an empty dictionary.

    Returns:
        Any: The parsed YAML data after applying the specified post-processing functions.
             If an error occurs during parsing or file reading, None is returned.

    Example Usage:
        # Basic usage with default post-processing functions
        parsed_data = parse_yaml_file('config.yaml')

        # Custom post-processing functions
        post_actions = {
            'post_read_function': lambda read_string: read_string.replace("old_value", "new_value"),
            'post_parse_function': lambda parsed: parsed['data']['key']
        }
        parsed_data = parse_yaml_file('config.yaml', post_actions)
    """
    if post_actions is None:
        post_actions = {}
    post_read_function = post_actions.get('post_read_function', lambda read_string: read_string)
    post_parse_function = post_actions.get('post_parse_function', lambda parsed: parsed)
    try:
        return post_parse_function(
            yaml.safe_load(
                post_read_function(
                    read_file(file_name)
                )
            )
        )
    except yaml.YAMLError:
        return None
