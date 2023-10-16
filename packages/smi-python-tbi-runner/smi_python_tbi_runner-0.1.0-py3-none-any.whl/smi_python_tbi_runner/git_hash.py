import os
import subprocess

from setup import NAME


def main():
    try:
        git_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("utf-8")
        with open(os.path.join(os.path.dirname(__file__), NAME, 'version.py'), 'w') as file:
            file.write(f'VERSION = "{git_hash}"')
            file.write(f'HASH = "{git_hash}"')
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
