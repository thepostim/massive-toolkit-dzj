from pathlib import Path
import json
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Metadata:
    title: str
    author: str
    created: str  # ISO 8601 date string
    modified: str  # ISO 8601 date string
    description: str = ""
    tags: list[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class MassiveForMetadataReader:
    @staticmethod
    def read(path: Path) -> Metadata:
        """Reads metadata from a JSON file and returns a Metadata dataclass."""
        if not path.is_file():
            raise FileNotFoundError(f"The file {path} does not exist.")
        
        try:
            with path.open('r', encoding='utf-8') as file:
                data: Dict[str, Any] = json.load(file)
                return Metadata(**data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to decode JSON from {path}: {e}")
        except TypeError as e:
            raise ValueError(f"Invalid data structure in {path}: {e}")

    @staticmethod
    def write(path: Path, metadata: Metadata) -> bool:
        """Writes the Metadata dataclass to a JSON file."""
        try:
            with path.open('w', encoding='utf-8') as file:
                json.dump(metadata.__dict__, file, ensure_ascii=False, indent=4)
            return True
        except IOError as e:
            raise IOError(f"Failed to write to {path}: {e}")
