import argparse
import json
import os
import pathlib
import csv
from dataclasses import dataclass, asdict
from typing import List, Dict, Union

@dataclass
class MassiveFile:
    filename: str
    size: int
    created_at: str
    modified_at: str

class MassiveToolkit:
    def __init__(self, directory: str):
        self.directory = pathlib.Path(directory)

    def scan(self) -> List[MassiveFile]:
        """Scan the directory for Massive files."""
        if not self.directory.is_dir():
            raise ValueError(f"The directory {self.directory} does not exist or is not a directory.")
        
        massive_files = []
        for file in self.directory.glob('*.massive'):  # Assuming .massive is the file extension
            file_info = MassiveFile(
                filename=file.name,
                size=file.stat().st_size,
                created_at=str(file.stat().st_ctime),
                modified_at=str(file.stat().st_mtime)
            )
            massive_files.append(file_info)
        return massive_files

    def get_file_info(self, filename: str) -> Union[MassiveFile, None]:
        """Retrieve information about a specific Massive file."""
        file_path = self.directory / filename
        if not file_path.exists():
            raise FileNotFoundError(f"The file {filename} does not exist in the directory.")
        
        return MassiveFile(
            filename=file_path.name,
            size=file_path.stat().st_size,
            created_at=str(file_path.stat().st_ctime),
            modified_at=str(file_path.stat().st_mtime)
        )

    def export(self, data: List[MassiveFile], format: str) -> None:
        """Export data to JSON or CSV format."""
        if format not in ['json', 'csv']:
            raise ValueError("Unsupported format. Use 'json' or 'csv'.")

        output_file = self.directory / f"exported_data.{format}"
        if format == 'json':
            with open(output_file, 'w') as json_file:
                json.dump([asdict(file) for file in data], json_file, indent=4)
        elif format == 'csv':
            with open(output_file, 'w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=asdict(data[0]).keys())
                writer.writeheader()
                for file in data:
                    writer.writerow(asdict(file))

    def batch_process(self, filenames: List[str]) -> List[MassiveFile]:
        """Batch process multiple Massive files."""
        processed_files = []
        for filename in filenames:
            try:
                file_info = self.get_file_info(filename)
                processed_files.append(file_info)
            except FileNotFoundError as e:
                print(e)
        return processed_files

def main():
    parser = argparse.ArgumentParser(description="Massive for Windows Toolkit")
    subparsers = parser.add_subparsers(dest='command')

    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan directory for Massive files')
    scan_parser.add_argument('directory', type=str, help='Directory to scan')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show information about a specific file')
    info_parser.add_argument('directory', type=str, help='Directory containing the file')
    info_parser.add_argument('filename', type=str, help='Name of the file to get info about')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export data to JSON/CSV')
    export_parser.add_argument('directory', type=str, help='Directory containing the files')
    export_parser.add_argument('format', type=str, choices=['json', 'csv'], help='Format to export to')

    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch process multiple files')
    batch_parser.add_argument('directory', type=str, help='Directory containing the files')
    batch_parser.add_argument('filenames', type=str, nargs='+', help='Names of the files to process')

    args = parser.parse_args()

    toolkit = MassiveToolkit(args.directory)

    if args.command == 'scan':
        try:
            files = toolkit.scan()
            for file in files:
                print(file)
        except ValueError as e:
            print(e)

    elif args.command == 'info':
        try:
            file_info = toolkit.get_file_info(args.filename)
            print(file_info)
        except (ValueError, FileNotFoundError) as e:
            print(e)

    elif args.command == 'export':
        try:
            files = toolkit.scan()
            toolkit.export(files, args.format)
            print(f"Data exported to {args.directory}/exported_data.{args.format}")
        except (ValueError, IOError) as e:
            print(e)

    elif args.command == 'batch':
        processed_files = toolkit.batch_process(args.filenames)
        for file in processed_files:
            print(file)

if __name__ == '__main__':
    main()
