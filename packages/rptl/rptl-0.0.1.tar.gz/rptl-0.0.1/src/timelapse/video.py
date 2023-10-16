from pathlib import Path


class Video:
    def __init__(self, path: Path | str):
        if isinstance(path, str):
            path = Path(path)

        self.path = path

    def __repr__(self):
        return f"Video(path={self.path})"

    def __str__(self):
        return f"{self.path}"

    def __eq__(self, other):
        if not isinstance(other, Video):
            return NotImplemented
        return self.path == other.path

    @property
    def exists(self):
        return self.path.exists()

    def delete(self):
        self.path.unlink()

    def create(self):
        pass
        # self.path.touch()