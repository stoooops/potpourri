PROMPT_WRITE_COMMIT_MESSAGE = """
I want you to act as a technical writer for software engineers, your
primary responsibility is to write clear and concise commit messages
for code changes. Your job is to communicate the purpose and impact
of code changes to other members of the development team.

A good commit message has the following characteristics:
- It is concise and accurate.
- It is written in the imperative mood and begins with a verb
- It explains why the change was made, rather than how it was made.
- It includes a signature at the end of the message.

Here is an example of a good commit message:
```
🤖 Ensure non-empty password during login

The login form was submitting even if the password field was empty.
This commit fixes the bug by checking that the password field is not
empty before allowing the form to be submitted.


(commit message written by OpenAI {model})
```

Here is an example of a good commit message:
```text
🤖 Include latest dependencies for eslint, prettier

Updates the package.json file to include the latest
dependencies for prettier and eslint for code formatting.

prettier is a code formatter that automatically formats code to
conform to a consistent style. It is configured to use the
recommended settings for the JavaScript Standard Style.

eslint is a linter that checks for common errors and code smells.
It is configured to use the recommended settings for the
JavaScript Standard Style.


(commit message written by OpenAI {model})
```

Some other tips for writing good commit messages:
- Begin with "🤖 "
- Keep the subject line (the first line) to 50 characters or less
- Separate subject from body with a blank line
- Use the body of the message to explain the details of the commit
- Wrap the body at 72 characters                              like this
- Avoid words like "Update", "Refactor", "Fix", "Add", "Remove" in the
    subject line

At the end of the commit message, add two blank lines followed by a
signature:
```text
(commit message written by OpenAI {model})
```

Your first task is to review staged changes and suggest a commit
message for the latest patch.

Files changed:
```
// git status -s
{status_text}
```

Files diff:
```diff
// git diff --cached --no-color --no-ext-diff --unified=0 --no-prefix
{diff_text}
```

Choose a unique and stylish first line in the imperative tense
that concisely describes the changes made in the commit.
This line should be no more than 50 characters.

Now, please write a suggested commit message below that is clear,
concise, and colorful, following the rules described above,
beginning with "🤖 " and ending with the signature
"(commit message written by OpenAI {model})":

Respond with:
- A detailed paragraph explaining WHY the changes were made
- Ten unique, stylish, colorful, and concise subject lines
- A suggested commit message enclosed in ```text ... ```

Detailed explanation:
"""


class PromptBuilder:
    def get_prompt(self, model: str, status_text: str, diff_text: str) -> str:
        return PROMPT_WRITE_COMMIT_MESSAGE.format(
            model=model,
            status_text=status_text,
            diff_text=diff_text,
        )
