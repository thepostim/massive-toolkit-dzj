from pathlib import Path
from typing import Dict, Any, List, Callable
import json
import os

class MassiveForProcessor:
    def __init__(self, client: 'MassiveForClient'):
        """
        Initialize the MassiveForProcessor with a client instance.

        :param client: An instance of MassiveForClient used for processing.
        """
        self.client = client

    def process_file(self, path: Path) -> Dict[str, Any]:
        """
        Process a single file and return its extracted data.

        :param path: The path to the file to be processed.
        :return: A dictionary containing the extracted data.
        """
        try:
            text = self.extract_text(path)
            metadata = self.extract_metadata(path)
            return {
                "text": text,
                "metadata": metadata
            }
        except Exception as e:
            print(f"Error processing file {path}: {e}")
            return {}

    def extract_text(self, path: Path) -> str:
        """
        Extract text content from a given file.

        :param path: The path to the file.
        :return: The extracted text as a string.
        """
        try:
            with open(path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text
        except Exception as e:
            print(f"Error extracting text from {path}: {e}")
            return ""

    def extract_metadata(self, path: Path) -> Dict:
        """
        Extract metadata from a given file.

        :param path: The path to the file.
        :return: A dictionary containing the metadata.
        """
        try:
            metadata = {
                "filename": path.name,
                "size": os.path.getsize(path),
                "modified_time": os.path.getmtime(path)
            }
            return metadata
        except Exception as e:
            print(f"Error extracting metadata from {path}: {e}")
            return {}

    def batch_process(self, paths: List[Path], progress_callback: Callable[[int, int], None] = None) -> List[Dict]:
        """
        Process a batch of files and return a list of extracted data.

        :param paths: A list of paths to the files to be processed.
        :param progress_callback: An optional callback function to report progress.
        :return: A list of dictionaries containing the extracted data for each file.
        """
        results = []
        total_files = len(paths)

        for index, path in enumerate(paths):
            result = self.process_file(path)
            results.append(result)
            if progress_callback:
                progress_callback(index + 1, total_files)

        return results
