import os
import subprocess
import sys


def main():
    if len(sys.argv) < 3:
        print("Usage: python smi_python_commons/scm_version.py <NAME> <VERSION>")
        return
    name = sys.argv[1]
    version = sys.argv[2]
    current_directory = os.getcwd()
    try:
        git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
        with open(os.path.join(current_directory, name, 'project.py'), 'w') as file:
            file.write(f'NAME = "{name}"\n')
            file.write(f'VERSION = "{version}"\n')
            file.write(f'HASH = "{git_hash}"\n')
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
