# -*- coding: utf-8 -*-
import locale
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from codeboxcli.models.models import Base
from codeboxcli.models.models import Snippet
from codeboxcli.utils import default_editor
from codeboxcli.utils import messages

# Extract the language code part
language_code = locale.getlocale()
if language_code:
    language_code = language_code[0].split('_')[0]

# Create a database engine
engine = create_engine(
    f'sqlite:///{os.path.expanduser("~/.codebox/database.db")}')

# Create tables based on models
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)


def list_to_tags(tags):
    return ', '.join(tags)


def add(args):
    global language_code

    # Initialize variables to store name and tags
    name = None
    description = None
    tags = []

    if len(args) == 0:
        print(messages.help_add(language_code))
        return  # Exit the function

    # Initialize loop index
    i = 0
    while i < len(args):
        # Check if the current argument is "--help"
        if args[i] == "--help":
            print(messages.help_add(language_code))
            return  # Exit the function
        # Check if the current argument is "--name"
        elif args[i] == "--name":
            if i + 1 < len(args):
                # If there's a value after "--name", assign it to the 'name' variable
                name = args[i + 1]
                i += 2  # Skip both "--name" and its value
            else:
                print(messages.error_missing_value("--name", language_code))
                return  # Exit the function if there's an error
        # Check if the current argument is "--name"
        elif args[i] == "--description":
            if i + 1 < len(args):
                # If there's a value after "--description", assign it to the 'description' variable
                description = args[i + 1]
                i += 2  # Skip both "--description" and its value
            else:
                print(messages.error_missing_value(
                    "--description", language_code))
                return  # Exit the function if there's an error
        # Check if the current argument is "--tags"
        elif args[i] == "--tags":
            i += 1  # Move to the next argument (the first tag)
            # Loop until we encounter another argument starting with "--"
            while i < len(args) and not args[i].startswith("--"):
                tags.append(args[i])  # Add the tag to the 'tags' list
                i += 1  # Move to the next argument

            if len(tags) == 0:
                print(messages.error_missing_value("--tags", language_code))
                return  # Exit the function if there's an error
        else:
            # If the argument is not recognized, print an error message and exit
            print(messages.error_unknown_argument(args[i], language_code))
            return

    # Check if a valid name was provided
    if name is None:
        print(messages.error_missing_argument("--name", language_code))
    elif not ((name is None) and (description is None)):
        # Create a new Snippet instance and add it to the session
        with Session() as session:
            snippet = Snippet(
                name=name, content=description, tags=list_to_tags(tags))
            session.add(snippet)
            session.commit()
    else:
        edited_text = default_editor.open_default_editor("")

        if edited_text:
            # Create a new Snippet instance and add it to the session
            with Session() as session:
                snippet = Snippet(
                    name=name, content=edited_text, tags=list_to_tags(tags))
                session.add(snippet)
                session.commit()
        else:
            print(messages.error_saving(language_code))
