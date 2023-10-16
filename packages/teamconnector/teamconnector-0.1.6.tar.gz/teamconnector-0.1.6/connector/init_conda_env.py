"""
A module for setting environment variables for the active conda environment.

This module provides a `set_conda_env_vars` function that reads a `.env` file
located at a specified path and sets each non-commented line as an environment
variable for the active conda environment. Commented lines and empty lines are
skipped. If an error occurs while setting a variable, the function continues to
the next line and prints an error message.

The module also provides a `main` function that allows the `set_conda_env_vars`
function to be used as a command-line tool. The `main` function uses the
`argparse` module to parse command-line arguments and call the `set_conda_env_vars`
function with the specified file path.

Example usage
-------------
To set environment variables for the active conda environment based on a `.env`
file located at `/path/to/directory`, run the following command:

    python init_conda_env.py /path/to/directory
    python init_conda_env.py ~

Remember to deactivate and reactivate your conda environment to apply changes.
"""

import argparse
import subprocess
import os


def set_conda_env_vars(env_file_path='.'):
    """
    Set environment variables for the active conda environment based on a file.

    Parameters
    ----------
    env_file_path : str, optional
        The path to the directory containing the `.env` file. Defaults to the current directory.

    Raises
    ------
    FileNotFoundError
        If the `.env` file is not found at the specified path.

    Notes
    -----
    This function reads the `.env` file located at `env_file_path` 
    and sets each non-commented line as an environment variable 
    for the active conda environment. Commented lines and empty lines are skipped. 
    If an error occurs while setting a variable,
    the function continues to the next line and prints an error message.

    Example usage
    -------------
    >>> set_conda_env_vars('/path/to/directory')
    
    Remember to deactivate and reactivate your conda environment to apply changes.
    """
    env_file = os.path.join(env_file_path, '.env')

    if not os.path.exists(env_file):
        print(f"Error: .env file not found at {env_file_path}")
        return

    with open(env_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        # Skip comments and empty lines
        if line.startswith('#') or not line:
            continue

        try:
            # Set environment variable for the active conda environment
            subprocess.run(['conda', 'env', 'config',
                            'vars', 'set', line], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error setting variable: {line}")
            print(f"Error message: {e}")
            continue

    print("Remember to deactivate and reactivate your conda environment to apply changes.")


def main():
    parser = argparse.ArgumentParser(
        description='Set environment variables for the active conda environment based on a file.')
    parser.add_argument('env_file_path', metavar='env_file_path', type=str, nargs='?', default='.',
                        help='the path to the directory containing the `.env` file (default: current directory)')

    args = parser.parse_args()

    set_conda_env_vars(args.env_file_path)


if __name__ == '__main__':
    main()

