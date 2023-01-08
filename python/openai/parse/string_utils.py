from typing import List, Union


def wrap_text(lines: Union[str, List[str]], wrap_length: int) -> List[str]:
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
