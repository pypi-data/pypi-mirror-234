"""File utilities."""

from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import yaml

from .mapping_proxy import MappingProxy


def inflate_messages_from_key(yaml_file: Path, key: str) -> List[Dict[str, Any]]:
    """Returns inflated messages from a YAML file found under the given key, e.g. app.kelvin.parameters."""
    ret: List[Dict[str, Any]] = [{}]
    with open(yaml_file) as f:
        c = MappingProxy(yaml.safe_load(f))
        ret = c.get(key, {})
    return ret


class YamlFileWatcher:
    def __init__(self, file: Union[Path, str]) -> None:
        self.file_path = Path(file)

        self._stat = self._get_stat()
        self._hash = sha256(self.file_path.read_bytes()).digest()

    def get_updates(self, key: str) -> List[Dict[str, Any]]:
        return [{**r} for r in inflate_messages_from_key(self.file_path, key)]

    def _get_stat(self) -> Tuple[int, int]:
        """Get file stats."""

        stat = self.file_path.stat()

        return stat.st_mtime_ns, stat.st_size

    def check_stat(self) -> bool:
        """Check for updates by file modification time."""

        stat = self._get_stat()

        if stat != self._stat:
            hash = sha256(self.file_path.read_bytes()).digest()
            if hash == self._hash:
                return False

            self._stat, self._hash = stat, hash

            return True

        return False

    def get_data(self) -> Dict[str, Any]:
        """Get updated data."""

        with self.file_path.open("r") as file:
            return yaml.safe_load(file)
