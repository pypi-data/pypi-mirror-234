# -*- coding: utf-8 -*-
import os
import subprocess
import tempfile


def open_default_editor(initial_content=""):
    # Check if the EDITOR environment variable is set
    editor = os.environ.get("EDITOR")

    # If the EDITOR is not set, try to find a suitable editor from a list
    if editor is None:
        editors = ["nano", "vim", "emacs"]  # List of common editors
        for ed in editors:
            # Check if the editor is available in the system
            if subprocess.run(["which", ed], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                editor = ed
                break

    if editor:
        # Create a temporary file to hold the content
        with tempfile.NamedTemporaryFile(suffix=".txt", mode="w+", encoding="utf-8", delete=False) as temp_file:
            temp_file.write(initial_content)

        # Open the temporary file with the user's preferred editor
        subprocess.run([editor, temp_file.name])

        # Read the edited content from the temporary file
        with open(temp_file.name, "r", encoding="utf-8") as edited_file:
            edited_content = edited_file.read()

        # Remove the temporary file
        os.remove(temp_file.name)
        return edited_content
    else:
        return None
