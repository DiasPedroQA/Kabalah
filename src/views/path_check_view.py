# pylint: disable=C

# src/views/path_check_view.py

import json


def render_path_check(model):
    return json.dumps(model.to_dict()), 200, {'Content-Type': 'application/json'}
