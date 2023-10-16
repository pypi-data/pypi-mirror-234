#!/usr/bin/env python3
import textwrap
import json


def print_output(fileobj, *args, **kwargs):
    """
    saving print statemets to html_file
    """
    print(textwrap.dedent(*args), file=fileobj, **kwargs)


def save_as_json(pastro_dict, filename, *args, **kwargs):
    with open(filename, "w") as f:
        json.dump(obj=pastro_dict, fp=f, *args, **kwargs)
    return
