import re

from potpourri.python.openai.commit_message import CommitMessage
from potpourri.python.openai.completion import Completion
from potpourri.python.openai.parse.string_utils import wrap_text
from potpourri.python.openai.parse.validation import StartsWithRobotEmoji


class CompletionParser:
    """
    A class that parses the completion text.
    """

    def validate(self, text: str) -> None:
        StartsWithRobotEmoji().yes(text)

    def parse_commit_message(self, completion: Completion) -> CommitMessage:
        ### log to debug file
        with open("completion.txt", "w") as f:
            f.write(completion.text)

        # Initialize variables to store the three sections
        description = ""
        subject_lines = []
        commit_message = ""

        # Iterate through the lines and extract the three sections
        section = None
        for line in completion.text_lines():
            if line.endswith("ubject lines:"):
                section = "subject_lines"
            elif line.startswith("Suggested commit message:"):
                section = "commit_message"
            elif line.startswith("- ") and section == "subject_lines":
                subject_lines.append(line[2:])
            elif section == "commit_message":
                # ```text
                # foo
                # ```
                if line.startswith("```"):
                    continue
                # Wrap the line at 72 characters
                for wrapped in wrap_text(line, 72):
                    commit_message += wrapped + "\n"
            else:
                description += line + "\n"

        # Strip leading/trailing white space and remove the "(commit message written by OpenAI text-davinci-003)" line
        description = description.strip()
        commit_message = commit_message.strip()
        commit_message = re.sub(r"\(commit message written by OpenAI text-davinci-003\)", "", commit_message)
        # debugging below
        print("description: ", description)
        print("subject_lines: ", subject_lines)
        print("commit_message: ", commit_message)

        # should start with "🤖"
        self.validate(commit_message)

        # Return an instance of the CommitMessage class
        return CommitMessage(description, subject_lines, commit_message)


def main() -> None:
    # test
    pass


if __name__ == "__main__":
    main()
