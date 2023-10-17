class Argument:

    def __init__(self, name: str, short_flag: str, argument_type, argument_help: str, required: bool = False):
        self.name = name
        self.short_flag = short_flag
        self.argument_type = argument_type
        self.argument_help = argument_help
        self.required = required
