import os

from smi_python_commons.string.operations import trim_list, to_boolean, to_int, to_float, json_to_object


def set_environment_variable(variable_name: str, variable_value: str):
    os.environ[variable_name] = variable_value


def delete_environment_variable(variable_name: str):
    if variable_name in os.environ:
        os.environ.pop(variable_name)


def get_environment_variable(variable_name: str):
    return os.getenv(variable_name)


def get_boolean_environment_variable(variable_name: str):
    return to_boolean(get_environment_variable(variable_name))


def get_int_environment_variable(variable_name: str):
    return to_int(get_environment_variable(variable_name))


def get_float_environment_variable(variable_name: str):
    return to_float(get_environment_variable(variable_name))


def get_json_environment_variable(variable_name: str):
    return json_to_object(get_environment_variable(variable_name))


def get_environment_variables_list(variable_name: str, parse_function=None):
    env_variable = get_environment_variable(variable_name)
    if env_variable is None:
        return []
    trimmed_list = trim_list(env_variable.split(","))
    if parse_function is not None:
        return [parse_function(value, index) for index, value in enumerate(trimmed_list)]
    return trimmed_list
