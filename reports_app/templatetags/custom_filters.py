import json
from typing import Any, Dict, Union
from django import template

register = template.Library()


@register.filter
def parse_json(data: Union[str, Dict[str, Any]]) -> str:
    """
    Parses JSON data and formats it into a human-readable string.

    Args:
        data (Union[str, Dict[str, Any]]): The JSON data to be parsed.

    Returns:
        str: A formatted string representing the parsed JSON data.
             Each key-value pair from the 'comment' dictionary is formatted as 'key -> value'.
             If there are multiple key-value pairs, they are joined with line breaks.
             If the data cannot be parsed or if there are no results, a default "No results" message is returned.
    """
    try:
        if isinstance(data, str):
            data = json.loads(data)

        if isinstance(data, dict) and 'comment' in data:
            comments = data['comment']
            formatted_comments = []

            for comment in comments:
                for key, value in comment.items():
                    formatted_comments.append(f'{key} -> {value}')

            if formatted_comments:
                return '\n'.join(formatted_comments)

    except Exception:
        pass

    return "No results"
