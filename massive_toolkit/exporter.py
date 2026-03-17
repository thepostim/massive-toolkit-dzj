import json
import csv
from pathlib import Path
from typing import List, Dict
import pandas as pd

class DataExporter:
    """A class for exporting data to various file formats."""

    @staticmethod
    def to_json(data: List[Dict], path: Path) -> Path:
        """Export data to a JSON file.

        Args:
            data (List[Dict]): The data to export.
            path (Path): The path where the JSON file will be saved.

        Returns:
            Path: The path to the saved JSON file.
        """
        try:
            with path.open('w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            return path
        except IOError as e:
            raise RuntimeError(f"Failed to write JSON file at {path}: {e}")

    @staticmethod
    def to_csv(data: List[Dict], path: Path) -> Path:
        """Export data to a CSV file.

        Args:
            data (List[Dict]): The data to export.
            path (Path): The path where the CSV file will be saved.

        Returns:
            Path: The path to the saved CSV file.
        """
        try:
            with path.open('w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return path
        except IOError as e:
            raise RuntimeError(f"Failed to write CSV file at {path}: {e}")

    @staticmethod
    def to_excel(data: List[Dict], path: Path) -> Path:
        """Export data to an Excel file.

        Args:
            data (List[Dict]): The data to export.
            path (Path): The path where the Excel file will be saved.

        Returns:
            Path: The path to the saved Excel file.
        """
        try:
            df = pd.DataFrame(data)
            df.to_excel(path, index=False)
            return path
        except ImportError:
            raise RuntimeError("openpyxl is not installed. Please install it to export to Excel.")
        except Exception as e:
            raise RuntimeError(f"Failed to write Excel file at {path}: {e}")

    @staticmethod
    def to_txt(data: List[Dict], path: Path) -> Path:
        """Export data to a TXT file.

        Args:
            data (List[Dict]): The data to export.
            path (Path): The path where the TXT file will be saved.

        Returns:
            Path: The path to the saved TXT file.
        """
        try:
            with path.open('w', encoding='utf-8') as txt_file:
                for item in data:
                    txt_file.write(f"{item}\n")
            return path
        except IOError as e:
            raise RuntimeError(f"Failed to write TXT file at {path}: {e}")
