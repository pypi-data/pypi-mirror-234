# -*- coding: utf-8 -*-
import os

import tabulate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from codeboxcli.models.models import Base
from codeboxcli.models.models import Snippet

# Create a database engine
engine = create_engine(
    f'sqlite:///{os.path.expanduser("~/.codebox/database.db")}')

# Create tables based on models
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)


def list():
    # Fetches and displays a list of snippets from the database.
    with Session() as session:
        snippet_list = session.query(Snippet).all()

        data = []
        for snippet in snippet_list:
            content = snippet.content.split(
                "\n")[0][:100] if snippet.content else ""
            data.append([snippet.id, snippet.name, content, snippet.tags])

        headers = ["ID", "NAME", "CONTENT", "TAGS"]

        # Truncate the "CONTENTS" column to a certain length (e.g., 40 characters)
        truncated_data = [[row[0], row[1], row[2], row[3]] for row in data]

        table = tabulate.tabulate(
            truncated_data, headers=headers, tablefmt="grid")
        print(table)


if __name__ == "__main__":
    list()
