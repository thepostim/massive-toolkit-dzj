import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Callable, Optional, Any


@dataclass
class Result:
    path: Path
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None


class BatchProcessor:
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers

    def process_directory(self, path: Path, pattern: str = "*") -> List[Result]:
        results = []
        files_to_process = list(path.glob(pattern))
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {executor.submit(self.process_file, file): file for file in files_to_process}
            for future in as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append(Result(path=file, success=False, error=str(e)))
        
        return results

    def process_files(self, paths: List[Path], callback: Optional[Callable] = None) -> List[Result]:
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {executor.submit(self.process_file, file): file for file in paths}
            for future in as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    result = future.result()
                    if callback:
                        callback(result)
                    results.append(result)
                except Exception as e:
                    results.append(Result(path=file, success=False, error=str(e)))

        return results

    def process_file(self, file: Path) -> Result:
        try:
            # Simulate file processing logic (e.g., read JSON)
            with open(file, 'r') as f:
                data = json.load(f)
            return Result(path=file, success=True, data=data)
        except Exception as e:
            return Result(path=file, success=False, error=str(e))
