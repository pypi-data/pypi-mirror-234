# -*- coding: utf-8 -*-
import locale
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from codeboxcli.models.models import Base
from codeboxcli.models.models import Snippet
from codeboxcli.utils import default_editor
from codeboxcli.utils import messages
from codeboxcli.utils import pastebin

# Create a database engine
engine = create_engine(
    f'sqlite:///{os.path.expanduser("~/.codebox/database.db")}')

# Create tables based on models
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

# Extract the language code part
language_code = locale.getlocale()
if language_code:
    language_code = language_code[0].split('_')[0]


def share(args):
    global language_code

    if len(args) == 0:
        # Display help message and exit
        print(messages.help_share(language_code))
        return

    # Initialize default values for options
    expire_date = "1W"
    dev_key = os.getenv("CODEBOX_DEV_KEY")
    file_path = None

    # Initialize loop index
    i = 0
    while i < len(args):
        if args[i] == "--help":
            # Display help message and exit
            print(messages.help_share(language_code))
            return
        elif args[i] == "--expire-date":
            # Handle expiration date option
            if i + 1 < len(args):
                expire_date = args[i + 1]
                i += 2
            else:
                print(messages.error_missing_value(
                    "--expire-date", language_code))
                return
        elif args[i] == "--dev-key":
            # Handle dev key option
            i += 1
            if i < len(args):
                dev_key = args[i]
                i += 1
            else:
                print(messages.error_missing_value("--dev-key", language_code))
                return
        elif args[i] == "--share-file":
            # Handle share file option
            i += 1
            if i < len(args):
                file_path = args[i]
                i += 1
            else:
                print(messages.error_missing_value(
                    "--share-file", language_code))
                return
        else:
            i += 1

    # Check if we have to share a file
    if file_path != None:
        with open(file_path) as f:
            description = f.read()

            with Session() as session:
                snippet = Snippet(
                    name=file_path, content=description)
                session.add(snippet)
                session.commit()

                share_snippet(snippet.id, expire_date, dev_key)
        return
    else:
        share_snippet(args[0], expire_date, dev_key)


def share_snippet(id, expire_date, dev_key):
    global language_code

    # Share a Snippet instance
    with Session() as session:
        snippet = session.query(Snippet).get(id)

        if snippet:
            pastebin.post(snippet.name, snippet.content, expire_date, dev_key)
        else:
            print(messages.error_not_found(id, language_code))
