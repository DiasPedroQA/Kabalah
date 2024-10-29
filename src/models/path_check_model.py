# pylint: disable=C

# src/models/path_check_model.py


class PathCheckModel:
    def __init__(self, path: str, status: str):
        self.path = path
        self.status = status

    def to_dict(self):
        return {"path": self.path, "status": self.status}
