# -*- coding: utf-8 -*-
import locale
import os
import sys

# Define the path to the directory and the path to the configuration file within that directory
config_dir = os.path.expanduser("~/.codebox")

# Check if the directory doesn't exist, then create it
if not os.path.exists(config_dir):
    os.makedirs(config_dir)

from codeboxcli.commands import add
from codeboxcli.commands import delete
from codeboxcli.commands import edit
from codeboxcli.commands import list
from codeboxcli.commands import share
from codeboxcli.utils import messages

# Extract the language code part
language_code = locale.getlocale()
if language_code:
    language_code = language_code[0].split('_')[0]


def cli():
    global language_code

    # Check if there are at least 2 command line arguments (including the script name)
    if len(sys.argv) < 2:
        # Print the default help message
        print(messages.help_default(language_code))
        return  # Exit the function if no valid subcommand is provided

    subcommand = sys.argv[1]  # Get the subcommand from the second argument
    args = sys.argv[2:]  # Get the remaining arguments as a list

    if subcommand == "add":
        add.add(args)  # Call the 'add' function from the 'commands' module
    elif subcommand == "list":
        list.list()  # Call the 'list' function from the 'commands' module
    elif subcommand == "delete":
        # Call the 'delete' function from the 'commands' module
        delete.delete(args)
    elif subcommand == "edit":
        # Call the 'edit' function from the 'commands' module
        edit.edit(args)
    elif subcommand == "share":
        # Call the 'share' function from the 'commands' module
        share.share(args)
    elif subcommand == "--help":
        # Print the default help message
        print(messages.help_default(language_code))
    else:
        # Print an error message for an invalid subcommand
        print(messages.error_invalid_subcommand(language_code))


if __name__ == "__main__":
    cli()  # Call the 'cli' function when the script is executed directly
