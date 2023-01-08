import http.client
import json
import os
import re
import socket
import sys
import time
from typing import Any, Dict, List, Optional, Union

from potpourri.python.openai.commit_message import CommitMessage
from potpourri.python.openai.completion import Completion, CompletionRequest, CompletionResponse


class OpenAIApiException(Exception):
    """
    An exception that is raised when the OpenAI API returns an error.
    """

    pass


class OpenAIModelOverloadException(OpenAIApiException):
    """
    An exception that is raised when the OpenAI API returns a model overload error.
    """

    pass


class OpenAIBadCompletionException(OpenAIApiException):
    """
    An exception that is raised when the OpenAI API returns a bad completion.
    """

    pass


class OpenAIApiClient:
    """
    A simple wrapper around the OpenAI API
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Constructor for the OpenApiClient class.

        Parameters:
        api_key (str, optional): The OpenAI API key to be used. If not provided, the value of the
            OPENAI_API_KEY environment variable will be used.
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.host: str = "api.openai.com"
        self.conn = http.client.HTTPSConnection(host=self.host, port=443, timeout=30)
        self.route_completion = "/v1/completions"

    def _create_headers(self) -> Dict[str, str]:
        """Create the headers for the request to the OpenAI API."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def _send_request(self, request: CompletionRequest, headers: Dict[str, str]) -> CompletionResponse:
        """Send a POST request to the OpenAI API and return the response data as a CompletionResponse object."""
        data: bytes = json.dumps(request.to_dict()).encode("utf-8")
        self.conn.request("POST", self.route_completion, body=data, headers=headers)
        response: http.client.HTTPResponse = self.conn.getresponse()
        response_bytes: bytes = response.read()
        try:
            # {'id': 'cmpl-6ViayJ6ZhIl5HmAOpiA23oX4naca9', 'object': 'text_completion', 'created': 1673017612, 'model': 'text-davinci-003', 'choices': [{'text': 'response', 'index': 0, 'logprobs': None, 'finish_reason': 'length'}], 'usage': {'prompt_tokens': 3759, 'completion_tokens': 300, 'total_tokens': 4059}}
            response_data: Dict[str, Any] = json.loads(response_bytes)
            # {'error': {'message': 'That model is currently overloaded with other requests. You can retry your request, or contact us through our help center at help.openai.com if the error persists. (Please include the request ID 44fa8f95f731a58124b775d316c1b044 in your message.)', 'type': 'server_error', 'param': None, 'code': None}}
            if "error" in response_data:
                print(
                    f"\033[01;31mError: {response_data['error']['message']}\033[0;0m",
                    file=sys.stderr,
                )
                # try again
                if response_data["error"]["message"].startswith("That model is currently overloaded"):
                    raise OpenAIModelOverloadException(response_data["error"]["message"])

            completions = [
                Completion(c["text"], c["index"], c["logprobs"], c["finish_reason"]) for c in response_data["choices"]
            ]
            return CompletionResponse(completions)
        except json.JSONDecodeError:
            print(
                f"\033[01;31mError: Invalid JSON response from the API\033[0;0m",
                file=sys.stderr,
            )
            print(f"\033[01;31m{response_data}\033[0;0m", file=sys.stderr)
            raise OpenAIApiException("Error decoding JSON response from OpenAI API")
        except KeyError:
            print(
                f"\033[01;31mError: Invalid response from the API\033[0;0m",
                file=sys.stderr,
            )
            print(f"\033[01;31m{response_data}\033[0;0m", file=sys.stderr)
            raise OpenAIApiException("Error parsing JSON response from OpenAI API")

    def _check_response(self, response: CompletionResponse) -> bool:
        """Check if the response from the OpenAI API is valid."""
        if not response.completions:
            print(
                "\033[01;31mError: No completions returned from the API\033[0;0m",
                file=sys.stderr,
            )
            return False
        return True

    def parse_commit_message(self, completion: Completion) -> CommitMessage:
        # Initialize variables to store the three sections
        description = ""
        subject_lines = []
        commit_message = ""

        # Iterate through the lines and extract the three sections
        section = None
        for line in completion.text_lines():
            if line.startswith("Subject lines:"):
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
                for wrapped in self.wrap_text(line, 72):
                    commit_message += wrapped + "\n"
            else:
                description += line + "\n"

        # Strip leading/trailing white space and remove the "(commit message written by OpenAI text-davinci-003)" line
        description = description.strip()
        commit_message = commit_message.strip()
        commit_message = re.sub(r"\(commit message written by OpenAI text-davinci-003\)", "", commit_message)

        # Return an instance of the CommitMessage class
        return CommitMessage(description, subject_lines, commit_message)

    def wrap_text(self, lines: Union[str, List[str]], wrap_length: int) -> List[str]:
        """
        Wraps a list of strings at a specified wrap length, splitting only on spaces.

        Parameters:
        lines (str or list of str): The list of strings to wrap.
        wrap_length (int): The maximum length for each wrapped string.

        Returns:
        list of str: A list of the wrapped strings.
        """
        if isinstance(lines, str):
            lines = [lines]

        # Initialize a list to store the wrapped lines
        wrapped_lines = []

        # Iterate through each line in the list
        for line in lines:
            # Keep wrapping the line until it is shorter than the wrap length
            while len(line) > wrap_length:
                # Try to find the last space in the line that occurs before the wrap length
                space_index = line.rfind(" ", 0, wrap_length + 1)

                # If no space is found, just wrap the line at the wrap length
                if space_index == -1:
                    space_index = wrap_length

                # Add the wrapped line to the list
                wrapped_lines.append(line[:space_index])

                # Update the line to be the remaining portion after the wrapped line
                line = line[space_index:]
                # Add the final wrapped line to the list
                wrapped_lines.append(line)
        return wrapped_lines

    def get_suggested_commit_message(
        self,
        prompt: str,
        model: str = "text-davinci-003",
        max_tokens: int = 300,
        temperature: float = 0.9,
    ) -> CommitMessage:
        """
        Get a completion from the OpenAI API.

        Parameters:
        prompt (str): The prompt to complete.
        model (str, optional): The name of the model to use for generating the completion.
            Defaults to "text-davinci-003".
        max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 64.
        temperature (float, optional): The temperature to use for generating the completion.
            Defaults to 0.9.

        Returns:
        str: The completion generated by the OpenAI API.
        """
        MAX_RETRIES = 3
        TIMEOUT = 30

        delay = 1
        for i in range(MAX_RETRIES):
            if i > 0:
                delay *= 2
                time.sleep(delay)
                print(f"Retrying...")

            try:
                request_data: CompletionRequest = CompletionRequest(prompt, model, max_tokens, temperature)
                headers: Dict[str, str] = self._create_headers()
                response: CompletionResponse = self._send_request(request_data, headers)
                if not self._check_response(response):
                    raise OpenAIApiException("OpenAI API returned an invalid response")
                completion: Completion = response.completions[0]
                with open(".prompt", "a") as f:
                    f.write(completion.text)

                commit_message: CommitMessage = self.parse_commit_message(completion)

                return commit_message
            except socket.timeout as e:
                if time.time() > TIMEOUT:
                    raise e
                else:
                    print(f"\033[01;31mError: {e}\033[0;0m", file=sys.stderr)
            except Exception as e:
                if time.time() > TIMEOUT:
                    raise e
                else:
                    print(f"\033[01;31mError: {e}\033[0;0m", file=sys.stderr)

        raise OpenAIApiException("OpenAI API returned an invalid response")
