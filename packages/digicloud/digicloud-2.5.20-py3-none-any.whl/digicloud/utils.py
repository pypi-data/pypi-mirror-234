"""
    Common Utilitie functions.
"""
import re
import sys
import uuid

import requests


def tabulate(data):
    """Make dict or list to table ready tuples."""
    if isinstance(data, dict) and data:
        headers = data.keys()
        rows = [value for key, value in data.items()]
    elif isinstance(data, list) and data:
        headers = data[0].keys()
        rows = [[value for key, value in obj.items()] for obj in data]
    else:
        return (), ()

    return headers, rows


def is_tty():
    return sys.stdin.isatty()


def get_latest_version_number(package_name):
    uri = 'https://pypi.org/pypi/{}/json'.format(package_name)
    return requests.get(uri, timeout=1).json()['info']['version']


def compare_versions(left, right):
    v1_parts = list(map(int, left.split('.')))
    while len(v1_parts) < 3:
        v1_parts.append(0)

    v2_parts = list(map(int, right.split('.')))
    while len(v2_parts) < 3:
        v2_parts.append(0)
    return {
        'major': v1_parts[0] - v2_parts[0],
        'minor': v1_parts[1] - v2_parts[1],
        'patch': v1_parts[2] - v2_parts[2],
    }


def convert_camel_to_snake(name):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()


def t_or_f_or_n(arg):
    upper_arg = str(arg).upper()
    if 'TRUE'.startswith(upper_arg):
        return True
    elif 'FALSE'.startswith(upper_arg):
        return False
    else:
        return None
