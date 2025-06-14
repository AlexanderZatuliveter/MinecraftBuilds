import os


def get_resource_path(relative_path: str) -> str:
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
