def read_file(file_name: str, error_return: str = ""):
    try:
        with open(file_name, "r") as file:
            return file.read()
    except FileNotFoundError:
        return error_return
