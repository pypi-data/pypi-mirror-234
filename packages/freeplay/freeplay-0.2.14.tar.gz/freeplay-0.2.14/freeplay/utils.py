import re

from .errors import FreeplayError

variable_regex = re.compile(r"{{(\w+)}}")

def format_template_variables(template_content: str, variables: dict[str, str]) -> str:
    try:
        return variable_regex.sub(lambda match: variables[match.group(1)], template_content)
    except KeyError as e:
        raise FreeplayError(f"Missing variable with key: {e}.")
