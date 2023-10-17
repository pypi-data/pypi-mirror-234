import pathlib


def append(file: pathlib.Path, text: str) -> None:
    """
    Appends text to a file.

    Args:
        file (pathlib.Path): The path to the file.
        text (str): The text to append to the file.

    Returns:
        None
    """
    with open(file, "a") as f:
        f.write(text)
