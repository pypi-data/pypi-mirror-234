# -*- coding: utf-8 -*-
help_default = """
    Usage: codebox COMMAND [ARGS]

    Commands:
      add       Add an item.
      list      List items.
      delete    Delete an item.
      edit      Edit an item.
      share     Share an item
"""

help_add = """
    Usage: codebox add [ARGS]
    
    Arguments:
      --help                 Show this help message and exit.
      --name TEXT            Specify a name for the snippet. (Required)
      --description TEXT     Specify the content for the snippet.
      --tags TEXT            Add tags to categorize this snippet. Separate multiple tags with space.
    """

help_delete = """
    Usage: codebox delete [ARGS] SNIPPET_ID, ...
    
    Arguments:
      --help          Show this help message and exit.
    """

help_edit = """
    Usage: codebox edit [ARGS] SNIPPET_ID
    
    Arguments:
      --help          Show this help message and exit.
    """


help_share = """
    Usage: codebox share SNIPPET_ID [ARGS]
    
    Arguments:
      --help          Show this help message and exit.
      --expire-date   Specify the expire day.
      --dev-key       Specify the developer key.
      --share-file    Specify the file to share.
    """


error_invalid_subcommand = """
    Error: Invalid subcommand.
    """


error_missing_value = """
    Error: Missing value after {value}.
    """


error_missing_argument = """
    Error: Missing {value} argument.
    """


error_unknown_argument = """
    Error: Unknown argument {value}.
    """


error_saving = """
    Error: Snippet not saved.
    """


error_not_found = """
    Error: Snippet with ID {value} not found.
    """


share_url = """
    The snippet has been successfully shared.
    {value}.
    """


share_error = """
    Error: Unable to share the snippet.
           {value}.
    """
