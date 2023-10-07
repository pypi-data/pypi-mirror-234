import re
import sys
import logging


def extract_data(pattern, line):
    logging.debug('Extracting data from "%s"', line.strip())
    matched = re.search(pattern, line)
    if matched:
        data = matched.group()
        logging.debug('Extracted data "%s" from "%s"', data, line.strip())
        return data
    return None


def read_stdin_until_data_is_extracted():
    logging.debug("Reading stdin until data is extracted")

    url_pattern = r"https://[a-zA-Z0-9./_-]+"
    code_pattern = r"\b[A-Z0-9]{4}-[A-Z0-9]{4}\b"

    url = code = None

    for line in sys.stdin:
        url = url or extract_data(url_pattern, line)
        code = code or extract_data(code_pattern, line)

        if url and code:
            logging.debug("Data extracted url: %s user_code: %s", url, code)
            return url, code
