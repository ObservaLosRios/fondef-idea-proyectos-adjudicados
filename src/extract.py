import pandas as pd
from .interfaces import IDataSource
import os

class CSVExtractor(IDataSource):
    """Extracts data from a CSV file."""
    
    def __init__(self, file_path: str, **kwargs):
        self.file_path = file_path
        self.kwargs = kwargs

    def extract(self) -> pd.DataFrame:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        print(f"Extracting data from {self.file_path}...")
        return pd.read_csv(self.file_path, **self.kwargs)
