from typing import List


class CommitMessage:
    """A commit message consists of a description and one or more subject lines.

    Attributes:
        description (str): A brief description of the commit.
        subject_lines (list(str)): One or more lines describing the changes made in the commit.
        text (str): The full commit message, including both the description and the subject lines.
    """

    def __init__(self, description: str, subject_lines: List[str], text: str):
        self.description = description
        self.subject_lines = subject_lines
        self.text = text
