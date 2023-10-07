import re
import time
from math import trunc

from fovus.constants.cli_constants import TIMESTAMP

MILLISECONDS_IN_SECOND = 1000


class FovusCliArgumentParserUtil:
    @staticmethod
    def camel_to_snake(camel_case_str):
        uppercase_letters = "([A-Z])"
        snake_case_regex_substitution = r"_\1"
        snake_case_str = re.sub(uppercase_letters, snake_case_regex_substitution, camel_case_str).lower()
        if snake_case_str.startswith("_"):
            snake_case_str = snake_case_str[1:]
        return snake_case_str

    @staticmethod
    def set_timestamp(cli_dict):
        cli_dict[TIMESTAMP] = str(trunc(time.time() * MILLISECONDS_IN_SECOND))
        return cli_dict[TIMESTAMP]
