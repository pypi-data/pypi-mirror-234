"""Version of the module"""

import re

VERSION_OUTPUT_RE = r".*?(\d+\.\d+\.\d+\.\d+).*"


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


@static_vars(prog=re.compile(VERSION_OUTPUT_RE, re.MULTILINE))
def extract_version(input_str):
    result = None
    for match in extract_version.prog.finditer(input_str):
        result = match.group(1)
    return result
