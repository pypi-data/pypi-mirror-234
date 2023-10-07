import re
import sys


def extract_data(pattern, line):
    matched = re.search(pattern, line)
    return matched.group() if matched else None


def read_stdin_until_data_is_extracted():
    url_pattern = r"https://[a-zA-Z0-9./_-]+"
    code_pattern = r"\b[A-Z0-9]{4}-[A-Z0-9]{4}\b"

    url = code = None

    for line in sys.stdin:
        url = url or extract_data(url_pattern, line)
        code = code or extract_data(code_pattern, line)

        if url and code:
            return url, code