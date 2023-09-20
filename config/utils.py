import re


def format_filename(name: str) -> str:
    """
    Format a filename by removing a timestamp prefix.

    This function takes a filename as input and searches for a timestamp prefix
    in the format 'yyyy-MM-dd_HH-mm-ss_'. If found, it removes the prefix and returns
    the trimmed filename. If no matching prefix is found, the original filename
    is returned.

    Args:
        name (str): The input filename.

    Returns:
        str: The formatted filename with the timestamp prefix removed.

    Example:
        >>> format_filename('2023-09-15_14-30-45_example.txt')
        'example.txt'

        >>> format_filename('example.txt')
        'example.txt'
    """
    match = re.search(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_', name)
    if match:
        trimmed_name = name.replace(match.group(), "")
    else:
        trimmed_name = name
    return trimmed_name
