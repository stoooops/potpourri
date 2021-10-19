import os
from typing import List


def list_subdirs(root_dir: str) -> List[str]:
    result = []
    for file in os.listdir(root_dir):
        d = os.path.join(root_dir, file)
        if os.path.isdir(d):
            result.append(d)

    return result
