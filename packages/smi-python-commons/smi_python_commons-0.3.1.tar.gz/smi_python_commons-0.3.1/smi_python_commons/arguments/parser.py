import argparse

from smi_python_commons.arguments.config import Config, ConfigBase, SubCommandsConfig


def parse_arguments(argv, argv_config: ConfigBase):
    """
    Parses command-line arguments based on the provided configuration.

    Args:
        argv (list): List of command-line arguments.
        argv_config (Config): Configuration object containing argument definitions.

    Returns:
        argparse.Namespace: Parsed command-line arguments as a namespace object.
    """
    parser = argparse.ArgumentParser(description=argv_config.description)
    if isinstance(argv_config, Config):
        for argument in argv_config.arguments:
            parser.add_argument(
                ('-' + argument.short_flag),
                ('--' + argument.name),
                type=argument.argument_type,
                help=argument.argument_help,
                required=argument.required
            )
        args = parser.parse_args(argv[1:])
    elif isinstance(argv_config, SubCommandsConfig):
        # TODO : by example below : make it work
        subparsers = parser.add_subparsers(help=argv_config.description)
        for sub_parser_config in argv_config.sub_parsers_config:
            sub_parser = subparsers.add_parser(sub_parser_config.name, help=sub_parser_config.help)
            sub_parser.set_defaults(func=sub_parser_config.func)
            for argument in sub_parser_config.arguments:
                parser.add_argument(
                    ('-' + argument.short_flag),
                    ('--' + argument.name),
                    type=argument.argument_type,
                    help=argument.argument_help,
                    required=argument.required
                )
        '''
        parser = argparse.ArgumentParser(description='smi-cli-tool-xyz')
        subparsers = parser.add_subparsers(help='Available subcommands help')
        sub_parser = subparsers.add_parser('sub_command', help='Sub-command help')
        sub_parser.set_defaults(func=lambda args: None)
        sub_parser.add_argument('-o', '--outfile', required=True, help='Output file')
        sub_parser.add_argument('-i', '--infile', required=True, help='Input file')
        args = parser.parse_args(argv[1:])
        '''
        '''
        subparsers = parser.add_subparsers(help=argv_config.arguments.get('sub_parser_help', 'Available subcommands'))
        sub_parser = subparsers.add_parser(
            argv_config.arguments.get('sub_command', 'sub_command'),
            help=argv_config.arguments.get('sub_command_help', 'Sub-command help')
        )
        sub_parser.set_defaults(func=argv_config.arguments.get('sub_command_function', lambda arguments: None))
        for argument in argv_config.arguments:
            sub_parser.add_argument(
                ('-' + argument.short_flag),
                ('--' + argument.name),
                type=argument.argument_type,
                help=argument.argument_help,
                required=argument.required
            )
        '''
        args = parser.parse_args(argv[1:])
    else:
        raise TypeError("Not map or list.")
    return args
