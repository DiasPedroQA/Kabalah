# pylint: disable=C

import os


def validate_path(path):
    """Verifica se o caminho existe"""
    return os.path.exists(path)


def analyze_paths(paths):
    """
    Analisa uma lista de caminhos.
    :param paths: list[str]
    :return: list[dict]
    """
    results = []
    for path in paths:
        if os.path.exists(path):
            result = {
                "path": path,
                "exists": True,
                "is_file": os.path.isfile(path),
                "is_dir": os.path.isdir(path),
            }
            if result["is_file"]:
                result["size"] = os.path.getsize(path)
            results.append(result)
        else:
            results.append({"path": path, "exists": False})
    return results
